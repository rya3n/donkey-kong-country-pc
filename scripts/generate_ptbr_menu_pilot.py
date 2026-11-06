"""Generate private Rev 1 menu graphics for a separate experimental build.

Identified graphics/tilemaps and character messages change in a memory copy.
The input ROM and generated CPU translation units remain untouched.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct
from generate_ptbr_candy_pilot import make_candy_patch
from generate_ptbr_funky_pilot import make_funky_patch
from generate_ptbr_cranky_pilot import make_cranky_patch, make_cranky_tips_patch

ROOT = Path(__file__).resolve().parents[1]


def glyph(rom: bytes, offset: int, character: str) -> list[list[int]]:
    if character == " ":
        return [[0] * 8 for _ in range(16)]
    base = {"Ã": "A", "Ç": "C"}.get(character, character)
    if not 0x21 <= ord(base) <= 0x5f:
        raise ValueError(f"Unsupported pilot glyph: {character}")
    data = rom[offset + (ord(base) - 0x21) * 32:][:32]
    pixels = [[sum(((data[(plane//2)*16 + (y//2)*2 + plane%2] >> (7-x)) & 1) << plane
                   for plane in range(4)) for x in range(8)] for y in range(16)]
    if character == "Ã":
        # Preserve the entire A body inside the cell; reserve three rows for tilde.
        pixels = [[0]*8 for _ in range(3)] + [pixels[y*16//13][:] for y in range(13)]
        for x in (2,3,6): pixels[0][x] = 15
        for x in (1,4,5): pixels[1][x] = 15
    elif character == "Ç":
        pixels = [pixels[y*16//13][:] for y in range(13)] + [[0]*8 for _ in range(3)]
        pixels[13][4] = pixels[14][5] = pixels[15][3] = pixels[15][4] = 15
    return pixels


def encode_tile(pixels: list[list[int]]) -> bytes:
    out = bytearray(32)
    for y, row in enumerate(pixels):
        for x, value in enumerate(row):
            for plane in range(4):
                out[(plane//2)*16 + y*2 + plane%2] |= ((value >> plane) & 1) << (7-x)
    return bytes(out)


def make_patch(rom: bytes, config: dict) -> tuple[list[tuple[int, bytes]], dict]:
    changes = []
    summary = {}
    font_offset = int(config["glyph_source"]["offset"], 16)
    # Confirm the exact Rev 1 menu DMA pointers independently from v1.0 labels.
    for offset, expected in ((0xf746, "a9776a"), (0xf759, "a9776a"), (0xf7f0, "a9be7f")):
        if rom[offset:offset+3] != bytes.fromhex(expected):
            raise ValueError("Rev 1 menu pointer guard failed")
    if rom[0x39aa62:0x39aa69] != bytes.fromhex("b8 b2 87 00 1b e0 07"):
        raise ValueError("Rev 1 font DMA pointer guard failed")
    for screen in ("file_select", "player_select"):
        spec = config[screen]
        tm_start, gfx_start = int(spec["tilemap"],16), int(spec["graphics"],16)
        tm_size, gfx_size = int(spec["tilemap_size"],16), int(spec["graphics_size"],16)
        tilemap = list(struct.unpack_from(f"<{tm_size//2}H", rom, tm_start))
        graphics = bytearray(rom[gfx_start:gfx_start+gfx_size])
        if screen == "player_select":
            # The left side contains the Kongs. Reuse only text tiles not referenced there.
            text_cells = [i for i in range(len(tilemap)) if i%32 >= spec["clear_text_from_x"]]
            kept = {v&1023 for i,v in enumerate(tilemap) if i not in text_cells}
            available = sorted({tilemap[i]&1023 for i in text_cells} - kept - {0})
            for i in text_cells: tilemap[i] = 0
            glow_start, glow_size = int(spec["original_glow_tilemap"],16), int(spec["original_glow_tilemap_size"],16)
            # BG2 contains baked English lettering and its glow, not the characters.
            changes.append((glow_start, bytes(glow_size)))
        else:
            available = list(range(spec["reusable_tiles"][0], spec["reusable_tiles"][1]+1))
        characters = sorted(set("".join(label["text"].replace("\n", "") for label in spec["labels"])))
        if len(characters)*2 > len(available):
            raise ValueError("Not enough reserved glyph tiles")
        mapping = {}
        for character in characters:
            top, bottom = available[:2]; del available[:2]
            mapping[character] = top, bottom
            pixels = glyph(rom, font_offset, character)
            for index, rows in ((top, pixels[:8]), (bottom, pixels[8:])):
                graphics[index*32:index*32+32] = encode_tile(rows)
        for label in spec["labels"]:
            if "clear_width" in label:
                for y in range(label["y"], label["y"]+2):
                    for x in range(label["clear_x"], label["clear_x"]+label["clear_width"]):
                        tilemap[y*32+x] = 0
            for line, text in enumerate(label["text"].splitlines()):
                x, y = label["x"], label["y"] + line*2
                if x + len(text) > 32 or (y+2)*32 > len(tilemap):
                    raise ValueError(f"Label exceeds its tilemap: {label['id']}")
                for i, character in enumerate(text):
                    top, bottom = mapping[character]
                    tilemap[y*32+x+i] = top | label["palette"] << 10
                    tilemap[(y+1)*32+x+i] = bottom | label["palette"] << 10
        changes.extend(((tm_start, struct.pack(f"<{len(tilemap)}H", *tilemap)), (gfx_start, bytes(graphics))))
        summary[screen] = {"glyphs": len(characters), "labels": len(spec["labels"]),
                           "changed_tilemap_bytes": sum(a != b for a,b in zip(rom[tm_start:tm_start+tm_size], changes[-2][1])),
                           "changed_graphics_bytes": sum(a != b for a,b in zip(rom[gfx_start:gfx_start+gfx_size], graphics))}
    return changes, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", required=True, type=Path)
    args = parser.parse_args()
    rom = args.rom.read_bytes()
    profile = json.loads((ROOT/"config/roms/usa-rev1.json").read_text(encoding="utf-8"))
    if len(rom) != profile["bytes"] or hashlib.sha256(rom).hexdigest() != profile["sha256"]:
        parser.error("Expected the exact clean USA Rev 1 ROM")
    config = json.loads((ROOT/"localization/pt-BR/menu-pilot.json").read_text(encoding="utf-8"))
    changes, summary = make_patch(rom, config)
    candy_config=json.loads((ROOT/"localization/pt-BR/candy-pilot.json").read_text(encoding="utf-8"))
    candy_changes,candy_summary=make_candy_patch(rom,candy_config)
    changes.extend(candy_changes)
    funky_config=json.loads((ROOT/"localization/pt-BR/funky-pilot.json").read_text(encoding="utf-8"))
    funky_changes,funky_summary=make_funky_patch(rom,funky_config,candy_config)
    changes.extend(funky_changes)
    cranky_config=json.loads((ROOT/"localization/pt-BR/cranky-pilot.json").read_text(encoding="utf-8"))
    cranky_changes,cranky_summary=make_cranky_patch(rom,cranky_config,candy_config)
    changes.extend(cranky_changes)
    tips_config=json.loads((ROOT/"localization/pt-BR/cranky-tips-pilot.json").read_text(encoding="utf-8"))
    tips_changes,tips_summary=make_cranky_tips_patch(rom,tips_config,candy_config)
    changes.extend(tips_changes)
    occupied=set()
    for offset,data in changes:
        addresses=set(range(offset,offset+len(data)))
        if occupied & addresses: raise ValueError("Pilot patch regions overlap")
        occupied.update(addresses)
    patchset=hashlib.sha256(b"".join(struct.pack("<II",offset,len(data))+data for offset,data in changes)).hexdigest()
    out = ROOT/"experimental/usa-rev1/pt-BR/menu-pilot"
    out.mkdir(parents=True, exist_ok=True)
    header = ["/* Private derived graphics. Generated locally; never publish. */",
              f'#define PTBR_PATCHSET_ID "{patchset}"',
              f'#define PTBR_CANDY_MESSAGE_COUNT {candy_summary["messages"]}',
              f'#define PTBR_FUNKY_MESSAGE_COUNT {funky_summary["messages"]}',
              f'#define PTBR_CRANKY_MESSAGE_COUNT {cranky_summary["messages"]+tips_summary["messages"]}',
              f'#define PTBR_CRANKY_TIP_COUNT {tips_summary["messages"]}',
              "typedef struct PtbrMenuPatch { unsigned offset, size; const unsigned char *bytes; const char *before; } PtbrMenuPatch;"]
    for i, (offset,data) in enumerate(changes):
        header.append(f"static const unsigned char s_ptbr_data_{i}[] = {{")
        header.extend(",".join(f"0x{x:02x}" for x in data[j:j+24])+"," for j in range(0,len(data),24))
        header.append("};")
    header.append("static const PtbrMenuPatch s_ptbr_patches[] = {")
    for i,(offset,data) in enumerate(changes):
        before=hashlib.sha256(rom[offset:offset+len(data)]).hexdigest()
        header.append(f'{{{offset},{len(data)},s_ptbr_data_{i},"{before}"}},')
    header.append("};\n")
    header_path=out/"ptbr_menu_data.h"
    header_text="\n".join(header)
    if not header_path.exists() or header_path.read_text(encoding="utf-8")!=header_text:
        header_path.write_text(header_text,encoding="utf-8")
    manifest={"rom_sha256":profile["sha256"],"scope":"Menu graphics, eight Candy, four Funky, six Cranky greetings and nine hints from Kongo Jungle/Monkey Mines",
              "screens":summary,"candy":candy_summary,"funky":funky_summary,"cranky":cranky_summary,
              "cranky_tips":tips_summary,"patchset_sha256":patchset,
              "regions":[{"offset":f"0x{offset:06X}","bytes":len(data),"after_sha256":hashlib.sha256(data).hexdigest()}
                         for offset,data in changes],"source_rom_written":False}
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(manifest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
