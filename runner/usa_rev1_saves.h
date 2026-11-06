#pragma once
#include <stddef.h>
#include <wchar.h>

/* The user directory must exist. Changes process CWD once; use absolute paths
 * for other files. Exclusive until Close. Only successful guest frames flush.
 */
int Rev1SavesOpen(const wchar_t *user_directory, char *error, size_t error_size);
int Rev1SavesFlush(int force, char *error, size_t error_size);
int Rev1SavesEnabled(void);
void Rev1SavesClose(void);
