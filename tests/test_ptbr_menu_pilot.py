"""Pilot layout and data-only boundaries with synthetic ROM bytes."""
import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
spec = importlib.util.spec_from_file_location("menu_pilot", ROOT/"scripts/generate_ptbr_menu_pilot.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PilotTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads((ROOT/"localization/pt-BR/menu-pilot.json").read_text(encoding="utf-8"))
        data = bytearray(4194304)
        for offset, expected in ((0xf746,"a9776a"),(0xf759,"a9776a"),(0xf7f0,"a9be7f")):
            data[offset:offset+3] = bytes.fromhex(expected)
        data[0x39aa62:0x39aa69]=bytes.fromhex("b8 b2 87 00 1b e0 07")
        self.rom = bytes(data)

    def test_only_five_data_regions(self):
        before = self.rom
        # Supply synthetic distinct text tiles, leaving tile zero for the Kongs' area.
        import struct
        data=bytearray(self.rom)
        for i in range(896):
            if i%32>=12: struct.pack_into('<H',data,0x2f86be+i*2,1+i%100)
        self.rom=bytes(data)
        before=self.rom
        patches, _ = module.make_patch(self.rom, self.config)
        expected = {(0x31c2c7,0x5c0),(0x31c987,0x20e0),(0x2f86be,0x700),(0x2f8dbe,0x24e0),(0x2fb29e,0x600)}
        self.assertEqual({(offset,len(data)) for offset,data in patches},expected)
        self.assertEqual(self.rom,before)
        file_gfx = dict(patches)[0x31c987]
        self.assertEqual(file_gfx[:132*32], self.rom[0x31c987:0x31c987+132*32])
        self.assertEqual(file_gfx[160*32:], self.rom[0x31c987+160*32:0x31c987+0x20e0])

    def test_bad_menu_pointer_rejected(self):
        with self.assertRaisesRegex(ValueError,"pointer guard"):
            module.make_patch(bytes(4194304),self.config)

    def test_unsupported_accent_rejected(self):
        with self.assertRaisesRegex(ValueError,"Unsupported"):
            module.glyph(self.rom,0x3887af,"Ê")

    def test_accent_marks_fit_cell(self):
        for c in "ÃÇ":
            glyph=module.glyph(self.rom,0x3887af,c)
            self.assertEqual((len(glyph),len(glyph[0])),(16,8))
            self.assertTrue(any(any(row) for row in glyph))

    def test_overlong_label_rejected(self):
        self.config["file_select"]["labels"][0]["x"] = 31
        with self.assertRaisesRegex(ValueError,"exceeds"):
            module.make_patch(self.rom,self.config)

    def test_planar_encoding(self):
        self.assertEqual(module.encode_tile([[15]*8 for _ in range(8)]),bytes([255]*32))
        self.assertEqual(module.encode_tile([[1]*8 for _ in range(8)]),bytes([255,0]*8+[0]*16))


if __name__ == "__main__":
    unittest.main()
