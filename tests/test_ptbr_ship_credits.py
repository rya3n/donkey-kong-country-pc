"""Preserve attribution columns and scroll boundaries with synthetic text."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from generate_ptbr_candy_pilot import encode_message
from generate_ptbr_ship_credits import START, STOP, make_ship_credits_patch
from inventory_rev1_text import decode_lines


class ShipCreditsTests(unittest.TestCase):
    def test_title_and_question_share_space_and_attributions_keep_their_columns(self):
        config = json.loads((ROOT / "localization/pt-BR/ship-credits-pilot.json").read_text(encoding="utf-8"))
        accents = json.loads((ROOT / "localization/pt-BR/candy-pilot.json").read_text(encoding="utf-8"))["accent_slots"]
        name = "TEST T. QA"
        original = (
            b"\xa0\xa0" + encode_message(["EXAMPLE"], {}, 24)
            + encode_message(["HELP" + "." * 10 + name], {}, 24) * 5
            + b"\xa0\0" + encode_message(["TRY IT!?"], {}, 24)
        )
        rom = bytearray(STOP + 1)
        rom[0x01EECF:0x01EED2] = bytes.fromhex("a9 fc ef")
        rom[0x01EEDD:0x01EEE0] = bytes.fromhex("a9 8e f0")
        rom[START:STOP] = original
        start, result = make_ship_credits_patch(bytes(rom), config, accents)

        self.assertEqual((start, len(result)), (START, STOP - START))
        groups = [decode_lines(group) for group in result.split(b"\0")[:-1]]
        title = config["title"].replace("é", chr(accents["é"]["code"]))
        self.assertEqual(groups[0], [" ", " ", title])
        for group in groups[1:6]:
            self.assertEqual(group[0][14:], name)
        self.assertEqual(groups[6], [" "])
        self.assertEqual(groups[7][0].strip(), config["question"])


if __name__ == "__main__":
    unittest.main()
