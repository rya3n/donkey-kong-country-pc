/* Synthetic SRAM fixture: no ROM or game data. Used by test_saves_io.py. */
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <wchar.h>
#include <io.h>
#include <fcntl.h>
#include "usa_rev1_saves.h"

static uint8_t s_ram[2048];
uint8_t *g_sram = s_ram;
int g_sram_size = sizeof s_ram;

int wmain(int argc, wchar_t **argv) {
    if (argc < 3) return 2;
    char error[512];
    if (!Rev1SavesOpen(argv[1], error, sizeof error)) {
        fprintf(stderr, "%s\n", error);
        return 3;
    }
    int ok = 1;
    if (!wcscmp(argv[2], L"read")) {
        _setmode(_fileno(stdout), _O_BINARY);
        ok = fwrite(s_ram, 1, sizeof s_ram, stdout) == sizeof s_ram;
    } else if (!wcscmp(argv[2], L"hold")) {
        puts("READY"); fflush(stdout); getchar();
    } else {
        unsigned seed = argc > 3 ? (unsigned)wcstoul(argv[3], NULL, 10) : 7;
        for (unsigned i = 0; i < sizeof s_ram; i++) s_ram[i] = (uint8_t)(i * 37u + seed);
        if (!wcscmp(argv[2], L"block") || !wcscmp(argv[2], L"retry")) {
            wchar_t temporary[96];
            swprintf_s(temporary, 96, L"saves/save.srm.%lu.tmp", GetCurrentProcessId());
            if (!CreateDirectoryW(temporary, NULL)) return 4;
            ok = !Rev1SavesFlush(0, error, sizeof error);
            RemoveDirectoryW(temporary);
            if (!wcscmp(argv[2], L"retry")) ok = ok && Rev1SavesFlush(1, error, sizeof error);
        } else {
            ok = Rev1SavesFlush(0, error, sizeof error);
        }
    }
    Rev1SavesClose();
    return ok ? 0 : 5;
}
