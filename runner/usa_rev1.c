/* USA Rev 1 experimental native bring-up.
 * Frame scheduling and native HDMA integration follow the MIT DKC1Recomp host.
 * The runtime is the pinned snesrecomp framework (see third-party notices).
 * No v1.0 gameplay-address hooks or widescreen adapters are installed here.
 */
#include "common_cpu_infra.h"
#include "common_rtl.h"
#include "cpu_state.h"
#include "input_playback.h"
#include "sha256.h"
#include "snes/dma.h"
#include "snes/interp_bridge.h"
#include "snes/ppu.h"
#include "snes/snes.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "usa_rev1.h"

enum { WIDTH = 256, HEIGHT = 224, FRAME_MASTER_CLOCKS = 1364 * 262 };
static uint32_t s_reset_pc, s_nmi_pc, s_resume_pc;
static uint64_t s_next_frame;
static int s_initialized, s_run_result = 1;
static uint8_t s_pixels[WIDTH * HEIGHT * 4];
static uint8_t *s_rom;
static double s_audio_fraction;

static void HashHex(const void *data, size_t size, char output[65]) {
    uint8_t hash[32];
    sha256_compute(data, size, hash);
    for (int i = 0; i < 32; i++) sprintf(output + i * 2, "%02x", hash[i]);
    output[64] = 0;
}

static uint8_t *ReadRomStream(FILE *file) {
    const char *expected = "df2644d435330192a13768cc1f79c5aa3084a64217a5250c6dd4ffdbe2175be4";
    if (!file) return NULL;
    if (fseek(file, 0, SEEK_END) || ftell(file) != 4194304L || fseek(file, 0, SEEK_SET)) {
        return NULL;
    }
    uint8_t *rom = malloc(4194304);
    if (!rom) return NULL;
    const size_t count = fread(rom, 1, 4194304, file);
    char digest[65];
    if (count != 4194304) { free(rom); return NULL; }
    HashHex(rom, count, digest);
    if (strcmp(digest, expected)) { free(rom); return NULL; }
    s_reset_pc = rom[0xfffc] | ((uint32_t)rom[0xfffd] << 8);
    s_nmi_pc = rom[0xffea] | ((uint32_t)rom[0xffeb] << 8);
    return rom;
}

static void Initialize(void) {
    s_initialized = 0;
    s_resume_pc = s_reset_pc;
    s_next_frame = 0;
    s_run_result = 1;
}

static void RunFrame(void) {
    const int first = !s_initialized;
    if (!s_next_frame) s_next_frame = g_cpu.master_cycles + FRAME_MASTER_CLOCKS;
    while (s_next_frame <= g_cpu.master_cycles) s_next_frame += FRAME_MASTER_CLOCKS;
    interp_bridge_set_master_deadline(s_next_frame);
    if (first) { cpu_state_init(&g_cpu, g_ram); s_initialized = 1; }
    if (!first && g_snes->nmiEnabled) {
        g_snes->inNmi = true;
        cpu_push_interrupt_frame_at(&g_cpu, s_resume_pc);
        s_run_result = interp_bridge_run_until_quiescent(&g_cpu, s_nmi_pc);
    } else {
        s_run_result = interp_bridge_run_until_quiescent(&g_cpu, s_resume_pc);
    }
    interp_bridge_set_master_deadline(0);
    s_resume_pc = interp_bridge_lle_resume_pc();
    if (g_cpu.master_cycles < s_next_frame) {
        g_cpu.master_cycles = s_next_frame;
        snes_sync_master_clock(g_snes, g_cpu.master_cycles);
    }
    s_next_frame += FRAME_MASTER_CLOCKS;
}

static void DrawFrame(void) {
    SimpleHdma channels[8];
    bool active[8];
    PpuSetExtraSpace(g_ppu, 0);
    PpuSetWidescreenPresentationXBias(g_ppu, 0);
    dma_startDma(g_dma, g_snesrecomp_last_hdmaen, true);
    for (int i = 0; i < 8; i++) {
        active[i] = g_dma->channel[i].hdmaActive;
        if (active[i]) SimpleHdma_Init(&channels[i], &g_dma->channel[i]);
    }
    for (int line = 0; line <= HEIGHT; line++) {
        ppu_runLine(g_ppu, line);
        for (int i = 0; i < 8; i++) if (active[i]) SimpleHdma_DoLine(&channels[i]);
    }
    (void)ppu_checkOverscan(g_ppu);
    ppu_handleVblank(g_ppu);
}

static const RtlGameInfo s_game = {
    .title = "dkc1-usa-rev1-experimental",
    .initialize = Initialize,
    .run_frame = RunFrame,
    .draw_ppu_frame = DrawFrame,
    .save_name_prefix = "dkc1-rev1-experimental"
};

void RunOneFrameOfGame_Internal(void) { RunFrame(); }
void ResetSpritesFunc(int first) { (void)first; }

int Rev1Open(FILE *file) {
    if (s_rom) return 0;
    s_rom = ReadRomStream(file);
    if (!s_rom) return 0;
    RtlRegisterGame(&s_game);
    if (!SnesInit(s_rom, 4194304)) { free(s_rom); s_rom = NULL; return 0; }
    PpuBeginDrawing(g_ppu, s_pixels, WIDTH * 4, kPpuRenderFlags_NewRenderer);
    RtlSetAudioOutputRate(32040);
    s_audio_fraction = 0;
    return 1;
}

const uint8_t *Rev1Pixels(void) { return s_pixels; }

int Rev1Step(uint32_t inputs, int16_t audio[2048], int *samples) {
    if (!s_rom) return 0;
    RtlRunFrame(inputs);
    if (g_fail || g_watchdog_tripped || !s_run_result) {
        fprintf(stderr, "execution stopped pc=%06x result=%d\n", s_resume_pc, s_run_result);
        return 0;
    }
    DrawFrame();
    s_audio_fraction += 32040.0 / 60.0988;
    *samples = (int)s_audio_fraction;
    s_audio_fraction -= *samples;
    memset(audio, 0, 2048 * sizeof *audio);
    RtlRenderAudio(audio, *samples, 2);
    return 1;
}

void Rev1Close(void) { free(s_rom); s_rom = NULL; }

#ifndef DKC_REV1_DESKTOP
static int WriteFrame(const char *prefix) {
    char path[1024];
    if (snprintf(path, sizeof path, "%s.ppm", prefix) >= (int)sizeof path) return 0;
    FILE *file = fopen(path, "wb");
    if (!file) return 0;
    int ok = fprintf(file, "P6\n%d %d\n255\n", WIDTH, HEIGHT) > 0;
    for (size_t i = 0; ok && i < WIDTH * HEIGHT; i++) {
        uint8_t rgb[3] = {s_pixels[i * 4 + 2], s_pixels[i * 4 + 1], s_pixels[i * 4]};
        ok = fwrite(rgb, 1, 3, file) == 3;
    }
    if (fclose(file)) ok = 0;
    return ok;
}

int main(int argc, char **argv) {
    if (argc < 4 || argc > 5) {
        fprintf(stderr, "usage: dkc_rev1_headless ROM FRAMES OUTPUT_PREFIX [INPUT_FILE]\n");
        return 2;
    }
    char *end;
    long frames = strtol(argv[2], &end, 10);
    if (*end || frames < 1 || frames > 20000) return 2;
    FILE *file = fopen(argv[1], "rb");
    int loaded = Rev1Open(file);
    if (file) fclose(file);
    if (!loaded) { fprintf(stderr, "Expected the exact USA Rev 1 ROM.\n"); return 2; }
    Dkc1InputPlayback playback = {0};
    char input_error[192];
    if (argc == 5 && !Dkc1InputPlaybackLoad(argv[4], &playback, input_error, sizeof input_error)) {
        fprintf(stderr, "input: %s\n", input_error);
        Rev1Close();
        return 2;
    }
    int16_t audio[1024 * 2];
    int audio_active_frames = 0;
    uint8_t audio_chain[32] = {0};
    uint8_t audio_hash_input[32 + sizeof audio];
    for (long frame = 0; frame < frames; frame++) {
        int samples;
        if (!Rev1Step(Dkc1InputPlaybackFrame(&playback, (size_t)frame), audio, &samples)) {
            Rev1Close();
            Dkc1InputPlaybackFree(&playback);
            return 4;
        }
        memcpy(audio_hash_input, audio_chain, sizeof audio_chain);
        memcpy(audio_hash_input + sizeof audio_chain, audio, (size_t)samples * 4);
        sha256_compute(audio_hash_input, sizeof audio_chain + (size_t)samples * 4, audio_chain);
        for (int i = 0; i < samples * 2; i++) {
            if (audio[i]) { audio_active_frames++; break; }
        }
        if ((frame + 1) % 60 == 0) {
            fprintf(stderr, "frame=%ld pc=%06x interpreted_steps=%llu wram0032=%04x\n",
                    frame + 1, s_resume_pc, interp_bridge_steps_total(),
                    g_ram[0x32] | ((unsigned)g_ram[0x33] << 8));
            fflush(stderr);
        }
    }
    char frame_hash[65], wram_hash[65], vram_hash[65], audio_hash[65];
    HashHex(s_pixels, sizeof s_pixels, frame_hash);
    HashHex(g_ram, sizeof g_ram, wram_hash);
    HashHex(g_ppu->vram, sizeof g_ppu->vram, vram_hash);
    for (int i = 0; i < 32; i++) sprintf(audio_hash + i * 2, "%02x", audio_chain[i]);
    audio_hash[64] = 0;
    if (!WriteFrame(argv[3])) { Rev1Close(); Dkc1InputPlaybackFree(&playback); return 5; }
    printf("{\"frames\":%ld,\"frame_sha256\":\"%s\",\"wram_sha256\":\"%s\","
           "\"vram_sha256\":\"%s\",\"audio_chain_sha256\":\"%s\","
           "\"interpreted_steps\":%llu,\"dispatch_entries\":%u,\"audio_active_frames\":%d}\n",
           frames, frame_hash, wram_hash, vram_hash, audio_hash, interp_bridge_steps_total(),
           g_dispatch_table_count, audio_active_frames);
    Rev1Close();
    Dkc1InputPlaybackFree(&playback);
    return 0;
}
#endif
