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
        rom[0x3c0344:0x3c0354]=bytes.fromhex("d1 31 f7 31 1d 32 4e 32 93 32 e3 32 d1 31 f7 31")
        self.source_widths={0x3c315b:[18,27],0x3c3189:[23,22,26],0x3c31d1:[11,26],
                            0x3c31f7:[22,15],0x3c321d:[18,18,12],0x3c324e:[20,25,23],
                            0x3c3293:[27,29,23],0x3c32e3:[27,29,24]}
        for message in self.config["messages"]:
            widths=self.source_widths[int(message["offset"],16)]
            lines=["X"*width for width in widths]
            name="Candy Kong" if message["offset"]=="0x3C315B" else "Honey Kong" if message["offset"]=="0x3C324E" else ""
            if name:lines[0]=name.ljust(widths[0])
            offset=int(message["offset"],16)
            rom[offset:offset+message["bytes"]]=candy.encode_message(lines,{},29)
        self.rom=bytes(rom)

    def test_exact_sizes_and_twelve_regions(self):
        patches,info=candy.make_candy_patch(self.rom,self.config)
        self.assertEqual({(offset,len(data)) for offset,data in patches},
                         {(0x3c315b,46),(0x3c3189,72),(0x3c31d1,38),(0x3c31f7,38),
                          (0x3c321d,49),(0x3c324e,69),(0x3c3293,80),(0x3c32e3,81),
                          (0x29da8c,16),(0x29da9c,16),(0x29daac,16),(0x29dabc,16)})
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

    def test_padding_only_adds_balanced_spaces(self):
        message=dict(lines=["Hello","World!"],bytes=30,max_line=29,balanced_padding=True)
        fitted=candy.fitted_lines(message)
        self.assertEqual([line.strip() for line in fitted],message["lines"])
        self.assertEqual(sum(map(len,fitted)),29)
        for original,line in zip(message["lines"],fitted):
            self.assertLessEqual(abs((len(line)-len(line.lstrip()))-(len(line)-len(line.rstrip()))),1)

    def test_padding_cannot_truncate(self):
        with self.assertRaisesRegex(ValueError,"does not fit"):
            candy.fitted_lines(dict(lines=["Long text"],bytes=3,max_line=29,balanced_padding=True))

    def test_padding_preserves_original_line_parity(self):
        message=dict(lines=["Hello","World!"],bytes=30,max_line=29,balanced_padding=True)
        fitted=candy.fitted_lines(message,[16,13])
        self.assertEqual([len(line)%2 for line in fitted],[0,1])
        self.assertEqual(sum(map(len,fitted)),29)

    def test_all_revisits_fit_real_source_line_parities(self):
        for message in self.config["messages"][2:]:
            widths=self.source_widths[int(message["offset"],16)]
            fitted=candy.fitted_lines(message,widths)
            self.assertEqual([len(line)%2 for line in fitted],[n%2 for n in widths])
            self.assertEqual([line.strip() for line in fitted],message["lines"])
            self.assertEqual(sum(map(len,fitted)),message["bytes"]-1)

    def test_honey_kong_preserved(self):
        self.config["messages"][5]["lines"][0]="Ei, Querido Kong!"
        with self.assertRaisesRegex(ValueError,"Protected name"):
            candy.make_candy_patch(self.rom,self.config)

    def test_revisit_pointer_must_match(self):
        rom=bytearray(self.rom);rom[0x3c0344]=0
        with self.assertRaisesRegex(ValueError,"revisit pointer"):
            candy.make_candy_patch(bytes(rom),self.config)


if __name__=="__main__":
    unittest.main()
