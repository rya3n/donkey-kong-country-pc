"""Pilot layout and data-only boundaries with synthetic ROM bytes."""
import importlib.util
import json
from pathlib import Path
import struct
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
        data[0xdfaa:0xdfb3] = bytes.fromhex("a2ef00a99eb8a0202c")
        data[0xdff8:0xdfff] = bytes.fromhex("bf9eb2ef09001c")
        data[0xe08c:0xe08f] = bytes.fromhex("ffe7ef")
        data[0x39aa62:0x39aa69]=bytes.fromhex("b8 b2 87 00 1b e0 07")
        data[0xf7a9:0xf7b2] = bytes.fromhex("a2 f1 00 a9 87 c8 a0 00 01")
        for index, tile in enumerate(range(219, 255)):
            struct.pack_into("<H", data, 0x31c887+index*2, tile | 7 << 10)
        struct.pack_into("<H", data, 0x31c2c7, 220)
        data[0x31ea67] = 219
        data[0x3887b2:0x3887b2+63*32] = bytes([255]) * (63*32)
        self.rom = bytes(data)

    def test_menu_regions_keep_glow_masks_aligned_by_player_mode(self):
        # Supply synthetic distinct text tiles, leaving tile zero for the Kongs' area.
        data=bytearray(self.rom)
        for i in range(896):
            if i%32>=12: struct.pack_into('<H',data,0x2f86be+i*2,1+i%100)
        for i in range(96):
            struct.pack_into("<H", data, 0x2fb29e+i*2, i+1)
        self.rom=bytes(data)
        before=self.rom
        patches, _ = module.make_patch(self.rom, self.config)
        expected = {(0x31c2c7,0x5c0),(0x31c887,0x100),(0x31c987,0x20e0),
                    (0x2f86be,0x700),(0x2f8dbe,0x24e0),(0x2fb29e,0x600),(0x2fb89e,0x2c20)}
        self.assertEqual({(offset,len(data)) for offset,data in patches},expected)
        self.assertEqual(self.rom,before)
        file_gfx = dict(patches)[0x31c987]
        self.assertEqual(file_gfx[:132*32], self.rom[0x31c987:0x31c987+132*32])
        title_map = dict(patches)[0x31c887]
        placed = {cell & 1023 for (cell,) in struct.iter_unpack("<H", title_map)} - {0}
        self.assertEqual(len(placed), 22)
        self.assertTrue(placed <= set(range(221, 255)))
        for tile in set(range(160, len(file_gfx)//32)) - placed:
            start = tile*32
            self.assertEqual(file_gfx[start:start+32], self.rom[0x31c987+start:0x31c987+start+32])
        player = dict(patches)[0x2f86be]
        glow_map, glow_gfx = (dict(patches)[offset] for offset in (0x2fb29e, 0x2fb89e))
        for label, glow_y in zip(self.config["player_select"]["labels"], (3, 10, 19)):
            for row in range(len(label["text"].splitlines()) * 2):
                x = label["x"]
                position = (glow_y+row)*32+x
                self.assertEqual(struct.unpack_from("<H", player, 2*((label["y"]+row)*32+x))[0] >> 10, 6)
                tile = struct.unpack_from("<H", glow_map, 2*position)[0]
                self.assertGreater(tile, 0)
                self.assertTrue(any(glow_gfx[tile*32:tile*32+32]))
        self.assertFalse(any(word for i, (word,) in enumerate(struct.iter_unpack("<H", glow_map)) if i%32 < 12))

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
