"""Replace the Rev 1 cast headings and remarks within their own text slots."""
from __future__ import annotations

from generate_ptbr_candy_pilot import encode_message
from inventory_rev1_text import inventory

START = 0x01DFD5
STOP = 0x01E1BC
POINTERS_START = 0x01DEBA
POINTERS_STOP = 0x01DFD4
HEADINGS = (0, 1, 9, 16, 23, 31, 37)
DIALOGUE = (42, 43, 45, 46)
MAX_COLUMNS = 29


def make_cast_patches(rom: bytes, config: dict, accents: dict) -> list[tuple[int, bytes]]:
    cast_region = {
        "id": "cast_en",
        "start": f"{START:x}",
        "end": f"{STOP:x}",
        "format": "high_bit_lines",
        "policy": "review_names_and_headings",
    }
    records = inventory(rom, [cast_region])
    if len(records) != 47 or sum(record["byte_length"] for record in records) != STOP - START:
        raise ValueError("Rev 1 cast layout guard failed")

    if len(config["headings"]) != len(HEADINGS) or len(config["dialogue"]) != len(DIALOGUE):
        raise ValueError("Expected seven cast headings and four remarks")
    pointers = rom[POINTERS_START:POINTERS_STOP]
    pointer_entries = {pointers[i:i+6] for i in range(0, len(pointers), 6)}

    patches = []
    for index, translated in zip(HEADINGS + DIALOGUE, config["headings"] + config["dialogue"]):
        record = records[index]
        offset = int(record["offset"], 16)
        size = record["byte_length"]
        if (offset & 0xFFFF).to_bytes(2, "little") * 3 not in pointer_entries:
            raise ValueError(f"Rev 1 cast pointer guard failed at {offset:#x}")
        if any(
            name.lower() in record["source"].lower() and name.lower() not in translated.lower()
            for name in ("Kongs", "Kremlings")
        ):
            raise ValueError("Cast group name must be preserved")
        if len(translated) > size:
            raise ValueError(f"Cast translation exceeds its {size}-character slot")
        # Each pointer still addresses the same line. Center the visible text
        # with padding and keep the high-bit terminator in its original byte.
        encoded = encode_message([translated.center(size)], accents, MAX_COLUMNS)
        patches.append((offset, encoded[:-1]))
    return patches
