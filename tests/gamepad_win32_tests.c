#define WIN32_LEAN_AND_MEAN
#include "gamepad_win32.h"
#include <stdio.h>
#include <stdlib.h>

#define CHECK(expr) do { \
    if (!(expr)) { \
        fprintf(stderr, "line %d: %s\n", __LINE__, #expr); \
        exit(EXIT_FAILURE); \
    } \
} while (0)

static XINPUT_GAMEPAD states[XUSER_MAX_COUNT];
static bool connected[XUSER_MAX_COUNT];
static unsigned reads;

static DWORD WINAPI ReadGamepad(DWORD index, XINPUT_STATE *state) {
    CHECK(index < XUSER_MAX_COUNT);
    ++reads;
    if (!connected[index]) return ERROR_DEVICE_NOT_CONNECTED;
    *state = (XINPUT_STATE){0};
    state->Gamepad = states[index];
    return ERROR_SUCCESS;
}

int main(void) {
    Rev1Gamepad gamepad = {0};
    CHECK(Rev1GamepadPoll(&gamepad, 0, ReadGamepad) == 0);
    CHECK(reads == 4);
    CHECK(Rev1GamepadPoll(&gamepad, 999, ReadGamepad) == 0);
    CHECK(reads == 4);

    connected[2] = true;
    states[2].wButtons = XINPUT_GAMEPAD_A;
    CHECK(Rev1GamepadPoll(&gamepad, 1000, ReadGamepad) == 0);
    CHECK(reads == 7 && gamepad.index == 2);
    CHECK(Rev1GamepadPoll(&gamepad, 1017, ReadGamepad) == 0);
    states[2].wButtons = 0;
    states[2].sThumbLX = XINPUT_GAMEPAD_LEFT_THUMB_DEADZONE;
    CHECK(Rev1GamepadPoll(&gamepad, 1034, ReadGamepad) == 0);

    const struct {
        WORD buttons;
        uint32_t expected;
    } mapping[] = {
        {XINPUT_GAMEPAD_A, 0x001}, {XINPUT_GAMEPAD_X, 0x002},
        {XINPUT_GAMEPAD_BACK, 0x004}, {XINPUT_GAMEPAD_START, 0x008},
        {XINPUT_GAMEPAD_DPAD_UP, 0x010}, {XINPUT_GAMEPAD_DPAD_DOWN, 0x020},
        {XINPUT_GAMEPAD_DPAD_LEFT, 0x040}, {XINPUT_GAMEPAD_DPAD_RIGHT, 0x080},
        {XINPUT_GAMEPAD_B, 0x100}, {XINPUT_GAMEPAD_Y, 0x200},
        {XINPUT_GAMEPAD_LEFT_SHOULDER, 0x400}, {XINPUT_GAMEPAD_RIGHT_SHOULDER, 0x800},
    };
    for (size_t i = 0; i < sizeof mapping / sizeof mapping[0]; ++i) {
        states[2].wButtons = mapping[i].buttons;
        CHECK(Rev1GamepadPoll(&gamepad, 1051 + i * 17, ReadGamepad) == mapping[i].expected);
    }
    states[2].wButtons = 0;
    states[2].sThumbLX = -8000;
    states[2].sThumbLY = 8000;
    CHECK(Rev1GamepadPoll(&gamepad, 1255, ReadGamepad) == 0x050);

    gamepad.require_neutral = true;
    CHECK(Rev1GamepadPoll(&gamepad, 1272, ReadGamepad) == 0);
    states[2] = (XINPUT_GAMEPAD){0};
    CHECK(Rev1GamepadPoll(&gamepad, 1289, ReadGamepad) == 0);
    states[2].sThumbLX = 8000;
    states[2].sThumbLY = -8000;
    CHECK(Rev1GamepadPoll(&gamepad, 1306, ReadGamepad) == 0x0a0);

    connected[0] = true;
    states[0].wButtons = XINPUT_GAMEPAD_START;
    CHECK(Rev1GamepadPoll(&gamepad, 1323, ReadGamepad) == 0x0a0);
    CHECK(gamepad.index == 2);
    connected[2] = false;
    CHECK(Rev1GamepadPoll(&gamepad, 1340, ReadGamepad) == 0);
    unsigned after_disconnect = reads;
    CHECK(Rev1GamepadPoll(&gamepad, 2339, ReadGamepad) == 0);
    CHECK(reads == after_disconnect);
    CHECK(Rev1GamepadPoll(&gamepad, 2340, ReadGamepad) == 0);
    CHECK(gamepad.index == 0);
    states[0].wButtons = 0;
    CHECK(Rev1GamepadPoll(&gamepad, 2357, ReadGamepad) == 0);
    states[0].wButtons = XINPUT_GAMEPAD_START;
    CHECK(Rev1GamepadPoll(&gamepad, 2374, ReadGamepad) == 0x008);
    connected[0] = false;
    CHECK(Rev1GamepadPoll(&gamepad, 2391, ReadGamepad) == 0);
    connected[0] = true;
    CHECK(Rev1GamepadPoll(&gamepad, 3391, ReadGamepad) == 0);
    states[0].wButtons = 0;
    CHECK(Rev1GamepadPoll(&gamepad, 3408, ReadGamepad) == 0);
    states[0].wButtons = XINPUT_GAMEPAD_A | XINPUT_GAMEPAD_DPAD_RIGHT;
    CHECK(Rev1GamepadPoll(&gamepad, 3425, ReadGamepad) == 0x081);
    return EXIT_SUCCESS;
}
