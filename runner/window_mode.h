#pragma once
#define WIN32_LEAN_AND_MEAN
#include <windows.h>

typedef struct Rev1WindowMode {
    int fullscreen;
    WINDOWPLACEMENT placement;
    LONG_PTR style;
    HMONITOR monitor;
} Rev1WindowMode;

/* Uses the window's current monitor; does not change the display resolution. */
int Rev1WindowFullscreen(HWND window, Rev1WindowMode *state, int enabled);
