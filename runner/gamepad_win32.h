#ifndef DKC_REV1_GAMEPAD_WIN32_H
#define DKC_REV1_GAMEPAD_WIN32_H

#include <stdbool.h>
#include <stdint.h>
#include <windows.h>
#include <xinput.h>

typedef DWORD (WINAPI *Rev1GamepadReadState)(DWORD index, XINPUT_STATE *state);

typedef struct Rev1Gamepad {
    DWORD index;
    ULONGLONG next_scan_ms;
    bool connected;
    bool require_neutral;
} Rev1Gamepad;

uint32_t Rev1GamepadPoll(Rev1Gamepad *gamepad, ULONGLONG now_ms,
                        Rev1GamepadReadState read_state);

#endif
