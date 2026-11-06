"""In-place dialogue and protected-name safeguards using synthetic data."""
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import generate_ptbr_candy_pilot as candy


class CandyPilotTests(unittest.TestCase):
    def setUp(self):
        self.config=json.loads((ROOT/"localization/pt-BR/candy-pilot.json").read_text(encoding="utf-8"))
        rom=bytearray(4194304)
        rom[0xee62:0xee6f]=bytes.fromhex("a2 e9 00 a9 dc d6 a0 00 06 22 ad 99 b9")
        rom[0x3c0354:0x3c0358]=bytes.fromhex("5b 31 89 31")
        rom[0x3c315b:0x3c3189]=candy.encode_message(["Candy Kong".ljust(18),"x".ljust(27)],{},29)
        rom[0x3c3189:0x3c31d1]=candy.encode_message(["A"*23,"B"*22,"C"*26],{},29)
        self.rom=bytes(rom)

    def test_exact_sizes_and_five_regions(self):
        patches,info=candy.make_candy_patch(self.rom,self.config)
        self.assertEqual({(offset,len(data)) for offset,data in patches},
                         {(0x3c315b,46),(0x3c3189,72),(0x29da8c,16),(0x29da9c,16),(0x29daac,16)})
        self.assertFalse(info["text_pointers_changed"])
        self.assertEqual(self.rom[0x3c0354:0x3c0358],bytes.fromhex("5b318931"))

    def test_name_change_rejected(self):
        self.config["messages"][0]["lines"][0]="Olá!  Sou a Doce Kong!"
        with self.assertRaisesRegex(ValueError,"Protected name"):
            candy.make_candy_patch(self.rom,self.config)

    def test_size_change_rejected(self):
        self.config["messages"][0]["lines"][1]+="!"
        with self.assertRaisesRegex(ValueError,"original 46-byte"):
            candy.make_candy_patch(self.rom,self.config)

    def test_long_line_rejected(self):
        with self.assertRaisesRegex(ValueError,"overlong"):
            candy.encode_message(["A"*30],{},29)

    def test_unknown_accent_rejected(self):
        with self.assertRaisesRegex(ValueError,"Unsupported"):
            candy.encode_message(["í"],self.config["accent_slots"],29)

    def test_used_source_slot_rejected(self):
        rom=bytearray(self.rom);rom[0x38a50b]=0x5b
        with self.assertRaisesRegex(ValueError,"already uses"):
            candy.make_candy_patch(bytes(rom),self.config)

    def test_incompatible_pointer_rejected(self):
        with self.assertRaisesRegex(ValueError,"pointer guard"):
            candy.make_candy_patch(bytes(4194304),self.config)

    def test_planar_roundtrip(self):
        pixels=[[(x+y)%4 for x in range(8)] for y in range(8)]
        self.assertEqual(candy.decode_tile(candy.encode_tile(pixels)),pixels)


if __name__=="__main__":
    unittest.main()
