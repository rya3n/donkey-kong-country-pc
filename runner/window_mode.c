#include "window_mode.h"

static int SetStyle(HWND window, LONG_PTR style) {
    SetLastError(0);
    return SetWindowLongPtrW(window, GWL_STYLE, style) != 0 || GetLastError() == 0;
}

static int RestorePlacement(HWND window, const Rev1WindowMode *state) {
    WINDOWPLACEMENT placement = state->placement;
    /* GetWindowPlacement may report SW_SHOWNORMAL even for a hidden window. */
    if (!(state->style & WS_VISIBLE)) placement.showCmd = SW_HIDE;
    return SetWindowPlacement(window, &placement) != 0;
}

int Rev1WindowFullscreen(HWND window, Rev1WindowMode *state, int enabled) {
    if (enabled) {
        HMONITOR monitor = MonitorFromWindow(window, MONITOR_DEFAULTTONEAREST);
        MONITORINFO info = {0};
        info.cbSize = sizeof info;
        if (!GetMonitorInfoW(monitor, &info)) return 0;
        int entering = !state->fullscreen;
        if (entering) {
            state->placement.length = sizeof state->placement;
            if (!GetWindowPlacement(window, &state->placement)) return 0;
            state->style = GetWindowLongPtrW(window, GWL_STYLE);
            LONG_PTR style = (state->style & ~(WS_OVERLAPPEDWINDOW | WS_MAXIMIZE | WS_MINIMIZE)) | WS_POPUP;
            if (!SetStyle(window, style)) return 0;
            state->fullscreen = 1;
        }
        state->monitor = monitor;
        RECT r = info.rcMonitor;
        if (!SetWindowPos(window, NULL, r.left, r.top, r.right - r.left, r.bottom - r.top,
                          SWP_NOZORDER | SWP_NOACTIVATE | SWP_FRAMECHANGED)) {
            if (entering) {
                SetStyle(window, state->style);
                RestorePlacement(window, state);
                state->fullscreen = 0;
            }
            return 0;
        }
    } else if (state->fullscreen) {
        if (!SetStyle(window, state->style)) return 0;
        state->fullscreen = 0;
        if (!RestorePlacement(window, state) ||
            !SetWindowPos(window, NULL, 0, 0, 0, 0,
                          SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_NOACTIVATE | SWP_FRAMECHANGED)) {
            return 0;
        }
    }
    return 1;
}
