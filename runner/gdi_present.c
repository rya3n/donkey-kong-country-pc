/* Offscreen GDI composition for the Rev 1 host. No guest memory is modified. */
#include "gdi_present.h"
#include <string.h>

void Rev1GdiFree(Rev1GdiSurface *surface) {
    if (surface->dc && surface->original) SelectObject(surface->dc, surface->original);
    if (surface->bitmap) DeleteObject(surface->bitmap);
    if (surface->dc) DeleteDC(surface->dc);
    memset(surface, 0, sizeof *surface);
}

static int EnsureSurface(Rev1GdiSurface *surface, HDC reference, int width, int height) {
    if (width < 1 || height < 1 || width > 16384 || height > 16384) return 0;
    if (surface->dc && surface->width == width && surface->height == height) return 1;
    Rev1GdiSurface fresh = {0};
    BITMAPINFO info = {0};
    info.bmiHeader.biSize = sizeof info.bmiHeader;
    info.bmiHeader.biWidth = width;
    info.bmiHeader.biHeight = -height;
    info.bmiHeader.biPlanes = 1;
    info.bmiHeader.biBitCount = 32;
    info.bmiHeader.biCompression = BI_RGB;
    void *bits = NULL;
    fresh.dc = CreateCompatibleDC(reference);
    if (fresh.dc) fresh.bitmap = CreateDIBSection(fresh.dc, &info, DIB_RGB_COLORS, &bits, NULL, 0);
    if (!fresh.bitmap || !bits) { Rev1GdiFree(&fresh); return 0; }
    fresh.original = SelectObject(fresh.dc, fresh.bitmap);
    if (!fresh.original || fresh.original == HGDI_ERROR) {
        fresh.original = NULL;
        Rev1GdiFree(&fresh);
        return 0;
    }
    fresh.width = width;
    fresh.height = height;
    /* Allocation failure above keeps the previous surface intact. */
    Rev1GdiFree(surface);
    *surface = fresh;
    return 1;
}

int Rev1GdiCompose(Rev1GdiSurface *surface, HDC reference, int width, int height,
                   const uint8_t *pixels, Rev1ScaleMode mode) {
    if (!EnsureSurface(surface, reference, width, height)) return 0;
    surface->complete = 0;
    RECT area = {0, 0, width, height};
    if (!FillRect(surface->dc, &area, (HBRUSH)GetStockObject(BLACK_BRUSH))) return 0;
    if (!pixels) {
        SetTextColor(surface->dc, RGB(255, 255, 255));
        SetBkMode(surface->dc, TRANSPARENT);
        DrawTextW(surface->dc, L"Preparando o jogo...", -1, &area,
                  DT_CENTER | DT_VCENTER | DT_SINGLELINE);
    } else {
        int draw_width = width, draw_height = height;
        if (mode == REV1_SCALE_4_3) {
            draw_height = width * 3 / 4;
            if (draw_height > height) { draw_height = height; draw_width = height * 4 / 3; }
        }
        if (draw_width > 0 && draw_height > 0) {
            BITMAPINFO info = {0};
            info.bmiHeader.biSize = sizeof info.bmiHeader;
            info.bmiHeader.biWidth = 256;
            info.bmiHeader.biHeight = -224;
            info.bmiHeader.biPlanes = 1;
            info.bmiHeader.biBitCount = 32;
            info.bmiHeader.biCompression = BI_RGB;
            SetStretchBltMode(surface->dc, COLORONCOLOR);
            int lines = StretchDIBits(surface->dc, (width - draw_width) / 2, (height - draw_height) / 2,
                draw_width, draw_height, 0, 0, 256, 224, pixels, &info, DIB_RGB_COLORS, SRCCOPY);
            if (lines == GDI_ERROR || lines == 0) return 0;
        }
    }
    if (!GdiFlush()) return 0;
    surface->complete = 1;
    return 1;
}

int Rev1GdiPresent(const Rev1GdiSurface *surface, HDC destination) {
    if (!surface->complete) return 0;
    /* The only write to the visible client is this completed frame. */
    if (!BitBlt(destination, 0, 0, surface->width, surface->height,
                surface->dc, 0, 0, SRCCOPY)) return 0;
    return GdiFlush() != 0;
}
