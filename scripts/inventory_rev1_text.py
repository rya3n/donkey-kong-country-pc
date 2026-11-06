"""Read-only inventory of identified Rev 1 text regions; output stays private.

Offsets are file offsets in the exact, headerless Rev 1 ROM. This is an
inventory reader, not a ROM patcher or a complete text/rendering decoder.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def decode_lines(data: bytes) -> list[str]:
    lines: list[str] = []
    current = ""
    for value in data:
        char = value & 0x7f
        if not 0x20 <= char <= 0x7e:
            raise ValueError(f"Unmapped control/glyph 0x{value:02x}; region requires review")
        current += chr(char)
        if value & 0x80:
            lines.append(current)
            current = ""
    if current:
        raise ValueError("Text region ends before its line terminator")
    return lines


def inventory(rom: bytes, regions: list[dict]) -> list[dict]:
    records = []
    for region in regions:
        start, end = int(region["start"], 16), int(region["end"], 16)
        if not 0 <= start < end <= len(rom):
            raise ValueError(f"Invalid region {region['id']}")
        cursor = start
        while cursor < end:
            if region["format"] == "nul_messages":
                stop = rom.index(0, cursor, end)
                payload_end, next_cursor = stop, stop + 1
            elif region["format"] == "high_bit_lines":
                stop = cursor
                while stop < end and not rom[stop] & 0x80:
                    stop += 1
                if stop == end:
                    raise ValueError("Missing line terminator")
                payload_end = next_cursor = stop + 1
            else:
                raise ValueError("Unknown text format")
            lines = decode_lines(rom[cursor:payload_end])
            if any(line.strip() for line in lines):
                records.append({
                    "id": f"{region['id']}.{cursor:06x}",
                    "region": region["id"], "offset": f"0x{cursor:06X}",
                    "end": f"0x{next_cursor:06X}", "byte_length": next_cursor - cursor,
                    "source_lines": lines, "source": " ".join(line.strip() for line in lines).strip(),
                    "policy": region["policy"], "translation": None,
                    "status": "preserve" if region["policy"] == "preserve_names" else "untranslated",
                    "review": ["in_game_context", "font_and_accents", "layout", "pointers_and_controls"],
                })
            cursor = next_cursor
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    # Extracted game text must not accidentally become public source content.
    out = args.out.resolve()
    if not any(out.is_relative_to(ROOT / name) for name in ("experimental", "evidence")):
        parser.error("Output must stay inside the ignored experimental/ or evidence/ directory")
    profile = json.loads((ROOT / "config/roms/usa-rev1.json").read_text(encoding="utf-8"))
    data = args.rom.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if len(data) != profile["bytes"] or digest != profile["sha256"]:
        parser.error("ROM does not match the exact headerless USA Rev 1 profile")
    regions = json.loads((ROOT / "localization/pt-BR/regions.json").read_text(encoding="utf-8"))
    records = inventory(data, regions["regions"])
    counts = {region["id"]: sum(r["region"] == region["id"] for r in records)
              for region in regions["regions"]}
    result = {"schema_version": 1, "rom_profile": "usa-rev1", "rom_sha256": digest,
              "complete_inventory": False, "runtime_modified": False,
              "region_counts": counts, "records": records}
    out.parent.mkdir(parents=True, exist_ok=True)
    # Refuse to overwrite a catalog that may already contain editorial work.
    with out.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"records": len(records), "regions": counts,
                      "complete_inventory": False, "runtime_modified": False}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
