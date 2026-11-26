"""Exercise fixed-width cast lines with a synthetic pointer and text table."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from generate_ptbr_candy_pilot import encode_message
from generate_ptbr_cast import DIALOGUE, HEADINGS, MAX_COLUMNS, POINTERS_START, START, STOP, make_cast_patches


class CastTests(unittest.TestCase):
    def test_translations_keep_terminators_pointers_and_all_name_bytes(self):
        config_dir = ROOT / "localization/pt-BR"
        config = json.loads((config_dir / "cast-pilot.json").read_text(encoding="utf-8"))
        accents = json.loads((config_dir / "candy-pilot.json").read_text(encoding="utf-8"))["accent_slots"]
        edited = dict(zip(HEADINGS + DIALOGUE, config["headings"] + config["dialogue"]))
        lengths = [max(8, len(edited.get(index, "")) + 1) for index in range(47)]
        remaining = STOP - START - sum(lengths)
        for index in range(remaining):
            lengths[index % len(lengths)] += 1
        rom = bytearray(STOP)
        offsets = []
        cursor = START
        for index, width in enumerate(lengths):
            offsets.append(cursor)
            original = f"QA{index:02}".ljust(width)
            rom[cursor:cursor+width] = encode_message([original], {}, MAX_COLUMNS)[:-1]
            pointer = (cursor & 0xffff).to_bytes(2, "little")
            entry = POINTERS_START + index * 6
            rom[entry:entry+6] = pointer * 3
            cursor += width
        self.assertEqual(cursor, STOP)
        original = bytes(rom)

        patches = make_cast_patches(original, config, accents)
        self.assertEqual({offset for offset, _ in patches}, {offsets[i] for i in edited})
        for offset, data in patches:
            rom[offset:offset+len(data)] = data
        self.assertEqual(rom[:START], original[:START])
        for index, (offset, width) in enumerate(zip(offsets, lengths)):
            with self.subTest(record=index):
                line = rom[offset:offset+width]
                if index in edited:
                    encoded = encode_message([edited[index].center(width)], accents, MAX_COLUMNS)
                    self.assertEqual(line, encoded[:-1])
                else:
                    self.assertEqual(line, original[offset:offset+width])
                self.assertFalse(any(byte & 0x80 for byte in line[:-1]))
                self.assertTrue(line[-1] & 0x80)

        damaged = bytearray(original)
        damaged[POINTERS_START] ^= 1
        with self.assertRaisesRegex(ValueError, "pointer guard"):
            make_cast_patches(bytes(damaged), config, accents)


if __name__ == "__main__":
    unittest.main()
