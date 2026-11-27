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
from generate_ptbr_cast import make_cast_patches
from generate_ptbr_funky_pilot import make_funky_patch
from generate_ptbr_cranky_pilot import make_cranky_patch, make_cranky_tips_patch
from generate_ptbr_ship_credits import make_ship_credits_patch
from generate_ptbr_ending_credits import make_ending_credits_patches

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


def write_glyph(graphics: bytearray, tiles: tuple[int, int], pixels: list[list[int]]) -> None:
    for tile, rows in zip(tiles, (pixels[:8], pixels[8:])):
        graphics[tile*32:tile*32+32] = encode_tile(rows)


def draw_label(
    tilemap: list[int], label: dict, mapping: dict[str, tuple[int, int]],
    palette: int, row_shift: int = 0,
) -> None:
    for line, text in enumerate(label["text"].splitlines()):
        x, y = label["x"], label["y"] + line * 2 - row_shift
        if x < 0 or y < 0 or x + len(text) > 32 or (y + 2) * 32 > len(tilemap):
            raise ValueError(f"Label exceeds its tilemap: {label['id']}")
        for i, character in enumerate(text):
            top, bottom = mapping[character]
            tilemap[y * 32 + x + i] = top | palette << 10
            tilemap[(y + 1) * 32 + x + i] = bottom | palette << 10


def make_player_glow(
    rom: bytes, spec: dict, glyphs: dict[str, list[list[int]]]
) -> list[tuple[int, bytes]]:
    glow = spec["glow"]
    tm_start, tm_size = int(glow["tilemap"], 16), int(glow["tilemap_size"], 16)
    gfx_start, gfx_size = int(glow["graphics"], 16), int(glow["graphics_size"], 16)
    original = struct.unpack_from(f"<{tm_size // 2}H", rom, tm_start)
    graphics = bytearray(rom[gfx_start:gfx_start + gfx_size])
    tiles = sorted({word & 1023 for word in original} - {0})
    if len(tiles) < 2 * len(glyphs) or tiles[-1] >= len(graphics) // 32 or any(graphics[:32]):
        raise ValueError("Invalid player-select highlight tiles")

    mapping = {}
    for index, (character, pixels) in enumerate(glyphs.items()):
        pair = tiles[2 * index], tiles[2 * index + 1]
        mapping[character] = pair
        write_glyph(graphics, pair, pixels)
    tilemap = [0] * len(original)
    for label in spec["labels"]:
        # The original HDMA exposes only the selected row range. BG2 scrolls
        # independently, so place each mask at its corresponding source rows.
        draw_label(tilemap, label, mapping, 0, label["glow_shift_y"])
    return [(tm_start, struct.pack(f"<{len(tilemap)}H", *tilemap)), (gfx_start, bytes(graphics))]


def make_candy_title(
    rom: bytes, spec: dict, font_offset: int, graphics: bytearray, file_tiles: set[int]
) -> tuple[int, bytes]:
    if rom[0xf7a9:0xf7b2] != bytes.fromhex("a2 f1 00 a9 87 c8 a0 00 01"):
        raise ValueError("Rev 1 Candy title DMA pointer guard failed")
    start, size = int(spec["tilemap"], 16), int(spec["tilemap_size"], 16)
    cells = struct.unpack_from(f"<{size//2}H", rom, start)
    icons = int(spec["slot_icons"], 16)
    # The slot portraits upload low bytes of tile indices into the shared map.
    protected = file_tiles | set(rom[icons:icons+int(spec["slot_icons_size"], 16)])
    title_tiles = {cell & 1023 for cell in cells}
    available = sorted((title_tiles - protected) & set(range(1, min(256, len(graphics)//32))))
    text = spec["text"]
    y = spec["y"]
    if not text.strip() or len(text) > 32 or y < 0 or (y+2)*32 > len(cells):
        raise ValueError("Candy title exceeds its tilemap")
    characters = sorted(set(text) - {" "})
    if len(characters)*2 > len(available):
        raise ValueError("Not enough exclusive Candy title tiles")
    if any(graphics[:32]):
        raise ValueError("Candy title requires a transparent tile zero")

    mappings = {}
    for index, character in enumerate(characters):
        top, bottom = available[2*index:2*index+2]
        mappings[character] = top, bottom
        write_glyph(graphics, (top, bottom), glyph(rom, font_offset, character))

    title_map = [0] * len(cells)
    x = (32-len(text))//2
    palette = spec["palette"] << 10
    for index, character in enumerate(text):
        if character != " ":
            top, bottom = mappings[character]
            title_map[y*32+x+index] = top | palette
            title_map[(y+1)*32+x+index] = bottom | palette
    return start, struct.pack(f"<{len(title_map)}H", *title_map)


def make_patch(rom: bytes, config: dict) -> tuple[list[tuple[int, bytes]], dict]:
    changes = []
    summary = {}
    font_offset = int(config["glyph_source"]["offset"], 16)
    # Confirm the exact Rev 1 menu DMA pointers independently from v1.0 labels.
    for offset, expected in (
        (0xf746, "a9776a"), (0xf759, "a9776a"), (0xf7f0, "a9be7f"),
        (0xdfaa, "a2ef00a99eb8a0202c"), (0xdff8, "bf9eb2ef09001c"), (0xe08c, "ffe7ef"),
    ):
        signature = bytes.fromhex(expected)
        if rom[offset:offset + len(signature)] != signature:
            raise ValueError("Rev 1 menu pointer guard failed")
    if rom[0x39aa62:0x39aa69] != bytes.fromhex("b8 b2 87 00 1b e0 07"):
        raise ValueError("Rev 1 font DMA pointer guard failed")
    for screen in ("file_select", "player_select"):
        spec = config[screen]
        tm_start, gfx_start = int(spec["tilemap"],16), int(spec["graphics"],16)
        tm_size, gfx_size = int(spec["tilemap_size"],16), int(spec["graphics_size"],16)
        original_tilemap = struct.unpack_from(f"<{tm_size//2}H", rom, tm_start)
        tilemap = list(original_tilemap)
        graphics = bytearray(rom[gfx_start:gfx_start+gfx_size])
        if screen == "player_select":
            # The left side contains the Kongs. Reuse only text tiles not referenced there.
            text_cells = [i for i in range(len(tilemap)) if i%32 >= spec["clear_text_from_x"]]
            kept = {v&1023 for i,v in enumerate(tilemap) if i not in text_cells}
            available = sorted({tilemap[i]&1023 for i in text_cells} - kept - {0})
            for i in text_cells: tilemap[i] = 0
        else:
            available = list(range(spec["reusable_tiles"][0], spec["reusable_tiles"][1]+1))
        characters = sorted(set("".join(label["text"].replace("\n", "") for label in spec["labels"])))
        if len(characters)*2 > len(available):
            raise ValueError("Not enough reserved glyph tiles")
        glyphs = {character: glyph(rom, font_offset, character) for character in characters}
        mapping = {}
        for character, pixels in glyphs.items():
            top, bottom = available[:2]; del available[:2]
            mapping[character] = top, bottom
            write_glyph(graphics, (top, bottom), pixels)
        for label in spec["labels"]:
            if "clear_width" in label:
                for y in range(label["y"], label["y"]+2):
                    for x in range(label["clear_x"], label["clear_x"]+label["clear_width"]):
                        tilemap[y*32+x] = 0
            draw_label(tilemap, label, mapping, label["palette"])
        if screen == "player_select":
            changes.extend(make_player_glow(rom, spec, glyphs))
        if screen == "file_select":
            candy_title = config["candy_save_title"]
            file_tiles = {word & 1023 for words in (original_tilemap, tilemap) for word in words}
            start, data = make_candy_title(rom, candy_title, font_offset, graphics, file_tiles)
            changes.append((start, data))
            summary["candy_save_title"] = {
                "labels": 1, "changed_tilemap_bytes": sum(a != b for a, b in zip(rom[start:start+len(data)], data)),
            }
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
    ship_credits = json.loads((ROOT/"localization/pt-BR/ship-credits-pilot.json").read_text(encoding="utf-8"))
    changes.append(make_ship_credits_patch(rom, ship_credits, candy_config["accent_slots"]))
    ending_credits = json.loads((ROOT/"localization/pt-BR/ending-credits-pilot.json").read_text(encoding="utf-8"))
    regions = json.loads((ROOT/"localization/pt-BR/regions.json").read_text(encoding="utf-8"))["regions"]
    changes.extend(make_ending_credits_patches(rom, ending_credits, candy_config, regions))
    cast = json.loads((ROOT/"localization/pt-BR/cast-pilot.json").read_text(encoding="utf-8"))
    changes.extend(make_cast_patches(rom, cast, candy_config["accent_slots"]))
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
    manifest={"rom_sha256":profile["sha256"],"scope":"Menu graphics, character dialogues, cast and credits",
              "screens":summary,"candy":candy_summary,"funky":funky_summary,"cranky":cranky_summary,
              "ship_credits":{"records":len(ship_credits["roles"])+2},
              "ending_credits":{"records":len(ending_credits["headings"])},
              "cast":{"headings":len(cast["headings"]),"remarks":len(cast["dialogue"])},
              "cranky_tips":tips_summary,"patchset_sha256":patchset,
              "regions":[{"offset":f"0x{offset:06X}","bytes":len(data),"after_sha256":hashlib.sha256(data).hexdigest()}
                         for offset,data in changes],"source_rom_written":False}
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(manifest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
