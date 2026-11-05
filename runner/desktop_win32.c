/* Windows test host. Execution is shared with the headless runner. */
#define WIN32_LEAN_AND_MEAN
#define NOMINMAX
#include <windows.h>
#include <commdlg.h>
#include <mmsystem.h>
#include <stdint.h>
#include <stdio.h>
#include <wchar.h>
#include <stdlib.h>
#include "common_rtl.h"
#include "sha256.h"
#include "usa_rev1.h"

enum { AUDIO_SLOTS = 8, PATH_CAP = 32768 };
static const wchar_t *s_title = L"Donkey Kong Country - Rev 1 experimental";
static HWND s_window;
static int s_running = 1, s_active, s_ready;
static uint32_t s_keys;
static HWAVEOUT s_device;
static HANDLE s_audio_event;
static struct { WAVEHDR header; int16_t pcm[2048]; } s_audio[AUDIO_SLOTS];
static wchar_t s_exe_dir[PATH_CAP], s_project_dir[PATH_CAP];
static unsigned long s_bench_frames;
static int s_start_cave;
static FILE *s_pacing;
static HANDLE s_frame_timer;
static int s_timer_period;
static int s_high_resolution;

static void OpenFrameClock(void) {
    s_frame_timer = CreateWaitableTimerExW(NULL, NULL,
        CREATE_WAITABLE_TIMER_HIGH_RESOLUTION, TIMER_MODIFY_STATE | SYNCHRONIZE);
    s_high_resolution = s_frame_timer != NULL;
    if (!s_frame_timer) {
        s_frame_timer = CreateWaitableTimerExW(NULL, NULL, 0,
            TIMER_MODIFY_STATE | SYNCHRONIZE);
        s_timer_period = timeBeginPeriod(1) == TIMERR_NOERROR;
    }
    fprintf(stderr, "frame_clock=%s target_hz=60.0988\n",
        s_high_resolution ? "high-resolution-waitable" : "timer-fallback");
}

static void CloseFrameClock(void) {
    if (s_frame_timer) { CancelWaitableTimer(s_frame_timer); CloseHandle(s_frame_timer); s_frame_timer = NULL; }
    if (s_timer_period) { timeEndPeriod(1); s_timer_period = 0; }
}

static void WaitForFrame(double remaining_ms) {
    LARGE_INTEGER due;
    due.QuadPart = -(LONGLONG)(remaining_ms * 10000.0);
    if (due.QuadPart == 0) due.QuadPart = -1;
    if (s_frame_timer && SetWaitableTimerEx(s_frame_timer, &due, 0, NULL, NULL, NULL, 0)) {
        /* Input wakes the message pump; only the QPC deadline allows a guest frame. */
        MsgWaitForMultipleObjectsEx(1, &s_frame_timer, INFINITE, QS_ALLINPUT, MWMO_INPUTAVAILABLE);
    } else {
        DWORD wait_ms = (DWORD)(remaining_ms > 16 ? 16 : remaining_ms);
        MsgWaitForMultipleObjectsEx(0, NULL, wait_ms ? wait_ms : 1, QS_ALLINPUT, MWMO_INPUTAVAILABLE);
    }
}

static uint32_t KeyMask(WPARAM key) {
    switch (key) {
    case VK_UP: return 1u << 4;
    case VK_DOWN: return 1u << 5;
    case VK_LEFT: return 1u << 6;
    case VK_RIGHT: return 1u << 7;
    case VK_RETURN: return 1u << 3;
    case VK_SHIFT: return 1u << 2;
    case 'Z': return 1u << 0;
    case 'X': return 1u << 1;
    case 'C': return 1u << 8;
    case 'V': return 1u << 9;
    case 'A': return 1u << 10;
    case 'S': return 1u << 11;
    default: return 0;
    }
}

static void Paint(HWND window, HDC dc) {
    RECT client;
    GetClientRect(window, &client);
    FillRect(dc, &client, (HBRUSH)GetStockObject(BLACK_BRUSH));
    if (!s_ready) {
        SetTextColor(dc, RGB(255, 255, 255));
        SetBkMode(dc, TRANSPARENT);
        DrawTextW(dc, L"Preparando o jogo...", -1, &client, DT_CENTER | DT_VCENTER | DT_SINGLELINE);
        return;
    }
    int width = client.right, height = width * 3 / 4;
    if (height > client.bottom) { height = client.bottom; width = height * 4 / 3; }
    if (width <= 0 || height <= 0) return;
    BITMAPINFO info = {0};
    info.bmiHeader.biSize = sizeof info.bmiHeader;
    info.bmiHeader.biWidth = 256;
    info.bmiHeader.biHeight = -224;
    info.bmiHeader.biPlanes = 1;
    info.bmiHeader.biBitCount = 32;
    info.bmiHeader.biCompression = BI_RGB;
    SetStretchBltMode(dc, COLORONCOLOR);
    StretchDIBits(dc, (client.right - width) / 2, (client.bottom - height) / 2,
        width, height, 0, 0, 256, 224, Rev1Pixels(), &info, DIB_RGB_COLORS, SRCCOPY);
}

static LRESULT CALLBACK WindowProc(HWND window, UINT message, WPARAM wp, LPARAM lp) {
    switch (message) {
    case WM_PAINT: {
        PAINTSTRUCT ps;
        HDC dc = BeginPaint(window, &ps);
        Paint(window, dc);
        EndPaint(window, &ps);
        return 0;
    }
    case WM_ERASEBKGND: return 1;
    case WM_KEYDOWN:
        if (wp == VK_ESCAPE) { DestroyWindow(window); return 0; }
        s_keys |= KeyMask(wp);
        return 0;
    case WM_KEYUP: s_keys &= ~KeyMask(wp); return 0;
    case WM_KILLFOCUS:
        s_keys = 0;
        s_active = 0;
        if (s_device) waveOutReset(s_device);
        return 0;
    case WM_SETFOCUS: s_active = 1; return 0;
    case WM_SIZE: InvalidateRect(window, NULL, FALSE); return 0;
    case WM_DESTROY: s_running = 0; PostQuitMessage(0); return 0;
    }
    return DefWindowProcW(window, message, wp, lp);
}

static void PumpMessages(void) {
    MSG message;
    while (PeekMessageW(&message, NULL, 0, 0, PM_REMOVE)) {
        if (message.message == WM_QUIT) { s_running = 0; break; }
        TranslateMessage(&message);
        DispatchMessageW(&message);
    }
}

static void ParentDirectory(wchar_t *path) {
    wchar_t *slash = wcsrchr(path, L'\\');
    if (slash) *slash = 0;
}

static int TryRom(const wchar_t *path) {
    FILE *file = _wfopen(path, L"rb");
    if (!file) return 0;
    int ok = Rev1Open(file);
    fclose(file);
    return ok;
}

static int LoadRom(void) {
    wchar_t directory[PATH_CAP], path[PATH_CAP];
    wcscpy_s(directory, PATH_CAP, s_exe_dir);
    for (int level = 0; level < 3; level++) {
        if (_snwprintf_s(path, PATH_CAP, _TRUNCATE, L"%s\\Donkey Kong Country (USA) (Rev 1).sfc", directory) >= 0 && TryRom(path))
            return 1;
        ParentDirectory(directory);
    }
    path[0] = 0;
    OPENFILENAMEW picker = {0};
    picker.lStructSize = sizeof picker;
    picker.hwndOwner = s_window;
    picker.lpstrTitle = L"Selecione a ROM USA Rev 1 (v1.1)";
    picker.lpstrFilter = L"ROM do SNES (*.sfc;*.smc)\0*.sfc;*.smc\0Todos os arquivos\0*.*\0";
    picker.lpstrFile = path;
    picker.nMaxFile = PATH_CAP;
    picker.Flags = OFN_FILEMUSTEXIST | OFN_PATHMUSTEXIST | OFN_NOCHANGEDIR;
    if (!GetOpenFileNameW(&picker)) return 0;
    if (TryRom(path)) return 1;
    MessageBoxW(s_window, L"Este arquivo nao corresponde a USA Rev 1 (v1.1) esperada. Confira a ROM.", s_title, MB_OK | MB_ICONERROR);
    return 0;
}

static void CloseAudio(void) {
    if (s_device) {
        waveOutReset(s_device);
        for (int i = 0; i < AUDIO_SLOTS; i++)
            if (s_audio[i].header.dwFlags & WHDR_PREPARED)
                waveOutUnprepareHeader(s_device, &s_audio[i].header, sizeof(WAVEHDR));
        waveOutClose(s_device);
        s_device = NULL;
    }
    if (s_audio_event) { CloseHandle(s_audio_event); s_audio_event = NULL; }
}

static int OpenAudio(void) {
    WAVEFORMATEX format = {0};
    format.wFormatTag = WAVE_FORMAT_PCM;
    format.nChannels = 2;
    format.nSamplesPerSec = 32040;
    format.wBitsPerSample = 16;
    format.nBlockAlign = 4;
    format.nAvgBytesPerSec = 32040 * 4;
    s_audio_event = CreateEventW(NULL, FALSE, FALSE, NULL);
    if (!s_audio_event) return 0;
    if (waveOutOpen(&s_device, WAVE_MAPPER, &format, (DWORD_PTR)s_audio_event, 0, CALLBACK_EVENT) != MMSYSERR_NOERROR) {
        s_device = NULL;
        CloseAudio();
        return 0;
    }
    for (int i = 0; i < AUDIO_SLOTS; i++) {
        s_audio[i].header.lpData = (LPSTR)s_audio[i].pcm;
        s_audio[i].header.dwBufferLength = sizeof s_audio[i].pcm;
        if (waveOutPrepareHeader(s_device, &s_audio[i].header, sizeof(WAVEHDR)) != MMSYSERR_NOERROR) {
            CloseAudio();
            return 0;
        }
    }
    return 1;
}

static int FreeAudioSlot(void) {
    for (int i = 0; i < AUDIO_SLOTS; i++)
        if (!(s_audio[i].header.dwFlags & WHDR_INQUEUE)) return i;
    return -1;
}

static int PrepareJungle(void) {
    wchar_t path[PATH_CAP];
    if (_snwprintf_s(path, PATH_CAP, _TRUNCATE, L"%s\\recipes\\usa-rev1\\boot-to-jungle.inputs", s_project_dir) < 0)
        return 0;
    FILE *file = _wfopen(path, L"rb");
    if (!file) return 0;
    unsigned int mask;
    unsigned long repeat, frames = 0;
    int16_t audio[2048];
    int samples;
    while (fscanf(file, "%x %lu", &mask, &repeat) == 2) {
        if (!repeat || repeat > 4800 || frames + repeat > 4800) { fclose(file); return 0; }
        while (repeat--) {
            const char *entrance = s_start_cave ? "EA" : getenv("DKC_REV1_TEST_ENTRANCE");
            if ((s_start_cave || s_bench_frames) && entrance && frames == 4202) {
                char *end;
                unsigned long value = strtoul(entrance, &end, 16);
                if (*end || value > 255) { fclose(file); return 0; }
                g_ram[0x3e] = (uint8_t)value;
                g_ram[0x3f] = 0;
            }
            if (!Rev1Step(mask, audio, &samples)) { fclose(file); return 0; }
            if (++frames % 30 == 0) {
                PumpMessages();
                if (!s_running) { fclose(file); return 0; }
            }
        }
    }
    fclose(file);
    fprintf(stderr, "warmup_frames=%lu\n", frames);
    return frames == 4800;
}

int WINAPI wWinMain(HINSTANCE instance, HINSTANCE previous, PWSTR command_line, int show) {
    (void)previous;
    s_start_cave = wcscmp(command_line, L"--caverna") == 0;
    SetProcessDPIAware();
    DWORD path_length = GetModuleFileNameW(NULL, s_exe_dir, PATH_CAP);
    if (!path_length || path_length >= PATH_CAP) return 2;
    ParentDirectory(s_exe_dir);
    wcscpy_s(s_project_dir, PATH_CAP, s_exe_dir);
    ParentDirectory(s_project_dir);
    ParentDirectory(s_project_dir);
    SetCurrentDirectoryW(s_exe_dir);
    FILE *log_stream = NULL;
    _wfreopen_s(&log_stream, L"DKC-Rev1-teste.log", L"w", stderr);
    const char *bench = getenv("DKC_REV1_BENCH_FRAMES");
    if (bench) {
        char *end;
        s_bench_frames = strtoul(bench, &end, 10);
        if (*end || !s_bench_frames || s_bench_frames > 20000) return 2;
    }
    WNDCLASSW window_class = {0};
    window_class.lpfnWndProc = WindowProc;
    window_class.hInstance = instance;
    window_class.lpszClassName = L"DkcRev1ExperimentalWindow";
    window_class.hCursor = LoadCursor(NULL, IDC_ARROW);
    window_class.hbrBackground = (HBRUSH)GetStockObject(BLACK_BRUSH);
    if (!RegisterClassW(&window_class)) return 2;
    RECT size = {0, 0, 768, 576};
    AdjustWindowRect(&size, WS_OVERLAPPEDWINDOW, FALSE);
    s_window = CreateWindowW(window_class.lpszClassName, s_title, WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, size.right - size.left, size.bottom - size.top,
        NULL, NULL, instance, NULL);
    if (!s_window) return 2;
    ShowWindow(s_window, show);
    UpdateWindow(s_window);
    if (!LoadRom()) { DestroyWindow(s_window); return 2; }
    if (wcscmp(command_line, L"--jungle") == 0 || s_start_cave) {
        SetWindowTextW(s_window, s_start_cave ? L"Preparando Reptile Rumble - aguarde alguns segundos" :
            L"Preparando Jungle Hijinxs - aguarde alguns segundos");
        if (!PrepareJungle()) {
            if (s_running) MessageBoxW(s_window, L"Nao foi possivel preparar a fase. Consulte DKC-Rev1-teste.log.", s_title, MB_OK | MB_ICONERROR);
            Rev1Close();
            if (s_running) DestroyWindow(s_window);
            return 3;
        }
    }
    s_ready = 1;
    SetWindowTextW(s_window, L"DKC Rev 1 - Setas: mover | Z: pular | X: correr/rolar | C: trocar | Enter: Start | Esc: sair");
    if (!OpenAudio())
        MessageBoxW(s_window, L"A saida de audio nao abriu. Voce pode testar a imagem e os controles sem som.", s_title, MB_OK | MB_ICONWARNING);
    fprintf(stderr, "desktop_ready=1 audio_device=%d\n", s_device != NULL);
    OpenFrameClock();
    fflush(stderr);
    LARGE_INTEGER frequency, now;
    QueryPerformanceFrequency(&frequency);
    QueryPerformanceCounter(&now);
    const double frame_ticks = (double)frequency.QuadPart / 60.0988;
    double next_frame = (double)now.QuadPart;
    double previous_present = 0, previous_finish = next_frame;
    unsigned long overruns = 0;
    const char *pacing_path = getenv("DKC1_PACING_LOG");
    if (pacing_path) {
        s_pacing = fopen(pacing_path, "w");
        if (!s_pacing) { CloseFrameClock(); CloseAudio(); Rev1Close(); DestroyWindow(s_window); return 5; }
        fprintf(s_pacing, "{\"schema\":\"dkc1.pacing.v1\",\"refresh_hz\":60.0988,\"host\":\"rev1-win32\"}\n");
    }
    int16_t discarded_audio[2048];
    int exit_code = 0;
    unsigned long frames = 0;
    while (s_running) {
        PumpMessages();
        if (!s_running) break;
        QueryPerformanceCounter(&now);
        if (!s_bench_frames && (!s_active || IsIconic(s_window))) {
            next_frame = (double)now.QuadPart;
            previous_present = 0;
            previous_finish = next_frame;
            MsgWaitForMultipleObjectsEx(0, NULL, 30, QS_ALLINPUT, MWMO_INPUTAVAILABLE);
            continue;
        }
        double remaining = (next_frame - (double)now.QuadPart) * 1000.0 / (double)frequency.QuadPart;
        if (remaining > 0) {
            WaitForFrame(remaining);
            continue;
        }
        int slot = s_device ? FreeAudioSlot() : 0;
        if (slot < 0) {
            MsgWaitForMultipleObjectsEx(1, &s_audio_event, 100, QS_ALLINPUT, MWMO_INPUTAVAILABLE);
            continue;
        }
        int samples;
        LARGE_INTEGER work_begin, cpu_finish, present_finish;
        QueryPerformanceCounter(&work_begin);
        int16_t *pcm = s_device ? s_audio[slot].pcm : discarded_audio;
        if (!Rev1Step(s_keys, pcm, &samples)) {
            CloseAudio();
            MessageBoxW(s_window, L"A execucao experimental parou. Consulte DKC-Rev1-teste.log.", s_title, MB_OK | MB_ICONERROR);
            exit_code = 4;
            break;
        }
        QueryPerformanceCounter(&cpu_finish);
        if (s_device) {
            WAVEHDR *header = &s_audio[slot].header;
            header->dwBufferLength = (DWORD)samples * 4;
            if (waveOutWrite(s_device, header, sizeof *header) != MMSYSERR_NOERROR) {
                fprintf(stderr, "audio_write_failed=1\n");
                CloseAudio();
            }
        }
        RedrawWindow(s_window, NULL, NULL, RDW_INVALIDATE | RDW_UPDATENOW);
        QueryPerformanceCounter(&present_finish);
        if (s_pacing) {
            const double tick_ms = 1000.0 / (double)frequency.QuadPart;
            double late = (work_begin.QuadPart - next_frame) * tick_ms;
            if (present_finish.QuadPart > next_frame + frame_ticks) overruns++;
            fprintf(s_pacing, "{\"frame\":%lu,\"work_ms\":%.6f,\"wait_ms\":%.6f,\"late_ms\":%.6f,"
                "\"present_interval_ms\":%.6f,\"overruns\":%lu,\"core_ms\":%.6f,\"gdi_audio_submit_ms\":%.6f}\n",
                frames, (present_finish.QuadPart - work_begin.QuadPart) * tick_ms,
                (work_begin.QuadPart - previous_finish) * tick_ms, late > 0 ? late : 0,
                previous_present ? (present_finish.QuadPart - previous_present) * tick_ms : 0,
                overruns, (cpu_finish.QuadPart - work_begin.QuadPart) * tick_ms,
                (present_finish.QuadPart - cpu_finish.QuadPart) * tick_ms);
        }
        previous_present = (double)present_finish.QuadPart;
        previous_finish = previous_present;
        next_frame += frame_ticks;
        /* An OS/audio stall must not be repaid by a burst of fast guest frames. */
        if (next_frame <= (double)present_finish.QuadPart)
            next_frame = (double)present_finish.QuadPart + frame_ticks;
        if (++frames % 600 == 0) { fprintf(stderr, "interactive_frames=%lu\n", frames); fflush(stderr); }
        if (s_bench_frames && frames >= s_bench_frames) break;
    }
    CloseAudio();
    CloseFrameClock();
    if (s_bench_frames) {
        uint8_t frame_hash[32], ram_hash[32];
        sha256_compute(Rev1Pixels(), 256 * 224 * 4, frame_hash);
        sha256_compute(g_ram, sizeof g_ram, ram_hash);
        fprintf(stderr, "benchmark_frame_sha256=");
        for (int i = 0; i < 32; i++) fprintf(stderr, "%02x", frame_hash[i]);
        fprintf(stderr, "\nbenchmark_wram_sha256=");
        for (int i = 0; i < 32; i++) fprintf(stderr, "%02x", ram_hash[i]);
        fprintf(stderr, "\n");
    }
    if (s_pacing) fclose(s_pacing);
    Rev1Close();
    if (IsWindow(s_window)) DestroyWindow(s_window);
    fprintf(stderr, "desktop_exit=%d frames=%lu\n", exit_code, frames);
    return exit_code;
}
