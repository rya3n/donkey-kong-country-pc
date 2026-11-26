"""Check the ending scroll's layout and attributions with synthetic credits."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from generate_ptbr_candy_pilot import encode_message
from generate_ptbr_ending_credits import (
    CEDILLA, ENDING_ACCENTS, MAX_COLUMNS, START, STOP, TILDE, make_ending_credits_patches,
)
from inventory_rev1_text import decode_lines


class EndingCreditsTests(unittest.TestCase):
    def test_translated_headings_preserve_every_attribution_and_scroll_limit(self):
        config_dir = ROOT / "localization/pt-BR"
        config = json.loads((config_dir / "ending-credits-pilot.json").read_text(encoding="utf-8"))
        dialogue = json.loads((config_dir / "candy-pilot.json").read_text(encoding="utf-8"))
        font = int(dialogue["font_offset"], 16)
        first_code = dialogue["font_first_code"]
        tilde = font + (TILDE - first_code) * 16
        cedilla = font + (CEDILLA - first_code) * 16
        rom = bytearray(tilde + 16)
        rom[0x01D5B6:0x01D5B9] = bytes.fromhex("a9 8f f0")
        rom[0x01D5C8:0x01D5CB] = bytes.fromhex("a9 05 f4")
        native_cedilla = b"\x18\x00" * 8
        rom[cedilla:cedilla+16] = native_cedilla

        headings = [
            len(heading) + (2 if index in (0, 1) else 0)
            for index, heading in enumerate(config["headings"])
        ]
        name_bytes = STOP - START - sum(headings) - len(headings)
        name_width, extra = divmod(name_bytes, len(headings) - 1)
        names = [b""]
        for index in range(len(headings) - 1):
            name = f"QA {index:02}".ljust(name_width + (index < extra), "X")
            names.append(encode_message([name], {}, MAX_COLUMNS)[:-1])
        rom[START:STOP] = b"".join(
            encode_message(["T" * width], {}, MAX_COLUMNS)[:-1] + name + b"\0"
            for width, name in zip(headings, names)
        )

        credits_patch, glyph_patch = make_ending_credits_patches(bytes(rom), config, dialogue, [])
        self.assertEqual((credits_patch[0], len(credits_patch[1])), (START, STOP - START))
        self.assertEqual((glyph_patch[0], len(glyph_patch[1])), (tilde, 16))
        self.assertTrue(any(glyph_patch[1]))
        self.assertEqual(rom[cedilla:cedilla+16], native_cedilla)

        groups = credits_patch[1].split(b"\0")
        self.assertEqual((len(groups), groups[-1]), (26, b""))
        accents = {**dialogue["accent_slots"], **ENDING_ACCENTS}
        for index, (group, heading, name) in enumerate(zip(groups, config["headings"], names)):
            with self.subTest(heading=heading):
                expected = heading.center(len(heading) + 4) if index == 0 else heading
                encoded = encode_message([expected], accents, MAX_COLUMNS)[:-1]
                self.assertEqual(group, encoded + name)
                self.assertTrue(all(len(line) <= MAX_COLUMNS for line in decode_lines(group)))


if __name__ == "__main__":
    unittest.main()
