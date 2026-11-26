"""Localize the ending credits headings and preserve the original attributions."""
from __future__ import annotations

from generate_ptbr_candy_pilot import decode_tile, encode_message, encode_tile
from inventory_rev1_text import decode_lines

START = 0x01F08F
STOP = 0x01F405
MAX_COLUMNS = 28
CEDILLA = 0x60
TILDE = 0x7B
ENDING_ACCENTS = {"ç": {"code": CEDILLA}, "ã": {"code": TILDE}}


def make_ending_credits_patches(
    rom: bytes, config: dict, dialogue: dict, regions: list[dict]
) -> list[tuple[int, bytes]]:
    if (rom[0x01D5B6:0x01D5B9] != bytes.fromhex("a9 8f f0")
            or rom[0x01D5C8:0x01D5CB] != bytes.fromhex("a9 05 f4")):
        raise ValueError("Rev 1 ending credits pointer guard failed")

    source = rom[START:STOP].split(b"\0")
    headings = config["headings"]
    if len(source) != 26 or source[-1] != b"" or rom[STOP] != 0 or len(headings) != 25:
        raise ValueError("Rev 1 ending credits layout guard failed")
    accents = {**dialogue["accent_slots"], **ENDING_ACCENTS}
    codes = {CEDILLA, TILDE}
    if any(item["code"] in codes for item in dialogue["accent_slots"].values()):
        raise ValueError("Ending credits collide with a dialogue glyph")
    for region in regions:
        start, stop = int(region["start"], 16), int(region["end"], 16)
        if any((byte & 0x7F) in codes for byte in rom[start:stop]):
            raise ValueError(f"Ending credits glyph slot already used in {region['id']}")

    first_lines = [decode_lines(group)[0] for group in source[:-1]]
    spare = sum(map(len, first_lines)) - sum(map(len, headings))
    if spare < 0:
        raise ValueError("Ending credits exceed their original ROM block")
    # Balance the unused bytes on the title. The game centers each line
    # independently, so the original name lines can be reused byte for byte.
    padded = [headings[0].center(len(headings[0]) + spare), *headings[1:]]
    parts = []
    for original, first, translated in zip(source, first_lines, padded):
        if "DONKEY KONG" in first and "DONKEY KONG" not in translated:
            raise ValueError("Ending credits heading must preserve the Donkey Kong name")
        header = encode_message([translated], accents, MAX_COLUMNS)
        parts.append(header[:-1] + original[len(first):] + b"\0")
    credits = b"".join(parts)
    if len(credits) != STOP - START:
        raise ValueError("Ending credits must retain their original block size")

    font = int(dialogue["font_offset"], 16)
    first_code = dialogue["font_first_code"]
    a_start = font + (ord("a") - first_code) * 16
    tilde_start = font + (TILDE - first_code) * 16
    if any(rom[tilde_start:tilde_start+16]):
        raise ValueError("Ending credits require a blank glyph slot for ã")
    # The native cedilla already occupies its own tile. Build only ã from
    # the lowercase a, reserving two rows for the tilde.
    unaccented = decode_tile(rom[a_start:a_start+16])
    pixels = [[0] * 8, [0] * 8] + [unaccented[y][:] for y in (1, 2, 3, 4, 6, 7)]
    for x, y in ((2, 1), (3, 0), (4, 0), (5, 1), (6, 0)):
        pixels[y][x] = 1
    return [(START, credits), (tilde_start, encode_tile(pixels))]
