/* Cartridge SRAM integration. Atomic I/O is the pinned MIT desktop_sram module.
 * This adapter keeps Rev 1 data isolated and protects one active writer.
 */
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdio.h>
#include <string.h>
#include "common_rtl.h"
#include "desktop_sram.h"
#include "usa_rev1_saves.h"

static Dkc1SramStore s_store;
static HANDLE s_lock = INVALID_HANDLE_VALUE;
static int s_enabled;

static int Fail(char *error, size_t size, const char *message) {
    if (error && size) snprintf(error, size, "%s", message);
    return 0;
}

int Rev1SavesOpen(const wchar_t *directory, char *error, size_t size) {
    if (s_enabled || s_lock != INVALID_HANDLE_VALUE)
        return Fail(error, size, "O salvamento ja esta aberto neste processo.");
    if (!directory || !SetCurrentDirectoryW(directory))
        return Fail(error, size, "Nao foi possivel abrir a pasta de dados do jogo.");
    if (!CreateDirectoryW(L"saves", NULL) && GetLastError() != ERROR_ALREADY_EXISTS)
        return Fail(error, size, "Nao foi possivel criar a pasta de saves.");
    s_lock = CreateFileW(L"saves/session.lock", GENERIC_READ | GENERIC_WRITE,
        FILE_SHARE_READ, NULL, OPEN_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if (s_lock == INVALID_HANDLE_VALUE)
        return Fail(error, size, "Nao foi possivel reservar os saves. Feche outra janela do jogo que use esta pasta e tente novamente.");
    if (!Dkc1SramLoad(&s_store, g_sram, (size_t)g_sram_size, error, size)) {
        Rev1SavesClose();
        return 0;
    }
    DWORD attributes = GetFileAttributesW(L"saves/save.srm");
    if (attributes != INVALID_FILE_ATTRIBUTES &&
        !CopyFileW(L"saves/save.srm", L"saves/save.srm.bak", FALSE)) {
        Rev1SavesClose();
        return Fail(error, size, "Nao foi possivel criar o backup do save. O arquivo original foi preservado.");
    }
    s_enabled = 1;
    fprintf(stderr, "[rev1-saves] enabled; backup at saves/save.srm.bak\n");
    return 1;
}

int Rev1SavesFlush(int force, char *error, size_t size) {
    return !s_enabled || Dkc1SramFlush(&s_store, g_sram, (size_t)g_sram_size,
                                      force != 0, error, size);
}

int Rev1SavesEnabled(void) { return s_enabled; }

void Rev1SavesClose(void) {
    s_enabled = 0;
    memset(&s_store, 0, sizeof s_store);
    if (s_lock != INVALID_HANDLE_VALUE) { CloseHandle(s_lock); s_lock = INVALID_HANDLE_VALUE; }
}
