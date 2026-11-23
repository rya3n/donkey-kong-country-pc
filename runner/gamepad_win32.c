#define WIN32_LEAN_AND_MEAN
#include "gamepad_win32.h"
#include "desktop_input.h"

enum { GAMEPAD_SCAN_INTERVAL_MS = 1000 };

uint32_t Rev1GamepadPoll(Rev1Gamepad *gamepad, ULONGLONG now_ms,
                        Rev1GamepadReadState read_state) {
    XINPUT_STATE state;

    if (gamepad->connected) {
        if (read_state(gamepad->index, &state) != ERROR_SUCCESS) {
            gamepad->connected = false;
            gamepad->next_scan_ms = now_ms + GAMEPAD_SCAN_INTERVAL_MS;
            return 0;
        }
    } else {
        if (now_ms < gamepad->next_scan_ms) return 0;
        gamepad->next_scan_ms = now_ms + GAMEPAD_SCAN_INTERVAL_MS;
        for (DWORD index = 0; index < XUSER_MAX_COUNT; ++index) {
            if (read_state(index, &state) != ERROR_SUCCESS) continue;
            gamepad->index = index;
            gamepad->connected = true;
            gamepad->require_neutral = true;
            break;
        }
        if (!gamepad->connected) return 0;
    }

    const XINPUT_GAMEPAD *pad = &state.Gamepad;
    uint32_t mask = Dkc1MapGamepad(pad->wButtons, pad->sThumbLX, pad->sThumbLY,
                                  XINPUT_GAMEPAD_LEFT_THUMB_DEADZONE);
    if (gamepad->require_neutral) {
        /* Discard held gameplay input on connection and after focus returns. */
        if (!mask) gamepad->require_neutral = false;
        return 0;
    }
    return mask;
}
