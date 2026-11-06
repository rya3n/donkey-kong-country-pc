#include "ptbr_pilot.h"
#include "sha256.h"
#include <stdio.h>
#include <string.h>
#include "ptbr_menu_data.h"

int Rev1ApplyPtbrMenuPilot(uint8_t *rom, size_t size) {
    for (size_t i = 0; i < sizeof s_ptbr_patches / sizeof s_ptbr_patches[0]; i++) {
        const PtbrMenuPatch *patch = &s_ptbr_patches[i];
        if (patch->offset > size || patch->size > size - patch->offset) return 0;
        uint8_t hash[32]; char hex[65];
        sha256_compute(rom + patch->offset, patch->size, hash);
        for (int j = 0; j < 32; j++) sprintf(hex + j*2, "%02x", hash[j]);
        hex[64] = 0;
        if (strcmp(hex, patch->before)) return 0;
    }
    for (size_t i = 0; i < sizeof s_ptbr_patches / sizeof s_ptbr_patches[0]; i++) {
        const PtbrMenuPatch *patch = &s_ptbr_patches[i];
        memcpy(rom + patch->offset, patch->bytes, patch->size);
    }
    fprintf(stderr, "ptbr_menu_pilot=1 data_regions=%zu source_rom_unchanged=1\n",
            sizeof s_ptbr_patches / sizeof s_ptbr_patches[0]);
    fprintf(stderr, "ptbr_candy_messages=%d ptbr_patchset_sha256=%s\n",
            PTBR_CANDY_MESSAGE_COUNT, PTBR_PATCHSET_ID);
    fprintf(stderr, "ptbr_funky_messages=%d\n", PTBR_FUNKY_MESSAGE_COUNT);
    fprintf(stderr, "ptbr_cranky_messages=%d\n", PTBR_CRANKY_MESSAGE_COUNT);
    fprintf(stderr, "ptbr_cranky_tips=%d\n", PTBR_CRANKY_TIP_COUNT);
    return 1;
}
