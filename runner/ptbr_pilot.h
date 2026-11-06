#pragma once
#include <stddef.h>
#include <stdint.h>

/* Experimental build only. Validate every region before modifying the copy. */
int Rev1ApplyPtbrMenuPilot(uint8_t *rom, size_t size);
