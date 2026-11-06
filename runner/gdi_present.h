#pragma once
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>

typedef struct Rev1GdiSurface {
    HDC dc;
    HBITMAP bitmap;
    HGDIOBJ original;
    int width, height, complete;
} Rev1GdiSurface;

typedef enum Rev1ScaleMode { REV1_SCALE_FILL, REV1_SCALE_4_3 } Rev1ScaleMode;

/* Compose never draws to reference_dc. Only a complete image may be presented. */
int Rev1GdiCompose(Rev1GdiSurface *surface, HDC reference_dc, int width, int height,
                   const uint8_t *bgra_pixels, Rev1ScaleMode mode);
int Rev1GdiPresent(const Rev1GdiSurface *surface, HDC destination);
void Rev1GdiFree(Rev1GdiSurface *surface);
