#pragma once
#include <stdint.h>
#include <stdio.h>

/* Call on one thread. The caller owns FILE; ROM data stays owned by the core. */
int Rev1Open(FILE *file);
const uint8_t *Rev1Pixels(void); /* 256 x 224, BGRA, top down. */
int Rev1Step(uint32_t inputs, int16_t audio[2048], int *stereo_frames);
void Rev1Close(void);
