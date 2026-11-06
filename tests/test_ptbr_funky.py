"""Funky boundaries, shared font and protected-name guards on synthetic data."""
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from generate_ptbr_candy_pilot import encode_message, fitted_lines
from generate_ptbr_funky_pilot import make_funky_patch
from inventory_rev1_text import decode_lines


class FunkyPilotTests(unittest.TestCase):
    def setUp(self):
        self.config=json.loads((ROOT/"localization/pt-BR/funky-pilot.json").read_text(encoding="utf-8"))
        self.font=json.loads((ROOT/"localization/pt-BR/candy-pilot.json").read_text(encoding="utf-8"))
        self.widths={0x3c3074:[12,21],0x3c3096:[25,27,14],0x3c30d9:[26,24,25],0x3c3125:[23,30]}
        rom=bytearray(4194304)
        rom[0xee62:0xee6f]=bytes.fromhex("a2 e9 00 a9 dc d6 a0 00 06 22 ad 99 b9")
        rom[0x3c036c:0x3c0374]=bytes.fromhex("74 30 96 30 d9 30 25 31")
        for m in self.config["messages"]:
            offset=int(m["offset"],16)
            lines=["X"*n for n in self.widths[offset]]
            name="Funky Kong" if offset==0x3c3074 else "Jumbo Barrel" if offset==0x3c3096 else None
            if name: lines[0]=name.ljust(self.widths[offset][0])
            rom[offset:offset+m["bytes"]]=encode_message(lines,{},30)
        self.rom=bytes(rom)

    def test_four_messages_only_and_shared_font_not_rewritten(self):
        patches,info=make_funky_patch(self.rom,self.config,self.font)
        self.assertEqual([(o,len(b)) for o,b in patches],list(zip(self.widths,[34,67,76,54])))
        self.assertEqual(info["accented_glyphs"],0)
        for m,(offset,data) in zip(self.config["messages"],patches):
            self.assertEqual(data[-1],0)
            self.assertNotIn(0,data[:-1])
            self.assertEqual(len(decode_lines(data[:-1])),len(self.widths[offset]))
            fitted=fitted_lines(m,self.widths[offset])
            self.assertEqual([n%2 for n in self.widths[offset]],[len(s)%2 for s in fitted])
            self.assertEqual([s.strip() for s in fitted],m["lines"])

    def test_character_and_vehicle_names_cannot_change(self):
        for index,old,new in ((0,"Funky Kong","Funky"),(1,"Jumbo Barrel","barril gigante")):
            with self.subTest(name=old):
                original=self.config["messages"][index]["lines"][:]
                self.config["messages"][index]["lines"]=[s.replace(old,new) for s in original]
                with self.assertRaisesRegex(ValueError,"Protected name"):
                    make_funky_patch(self.rom,self.config,self.font)
                self.config["messages"][index]["lines"]=original

    def test_pointer_change_rejected(self):
        rom=bytearray(self.rom);rom[0x3c036c]^=1
        with self.assertRaisesRegex(ValueError,"pointer guard"):
            make_funky_patch(bytes(rom),self.config,self.font)

    def test_overlapping_or_unknown_range_rejected(self):
        self.config["messages"][1]["offset"]="0x3C3074"
        with self.assertRaisesRegex(ValueError,"ranges"):
            make_funky_patch(self.rom,self.config,self.font)

    def test_missing_line_rejected(self):
        self.config["messages"][2]["lines"].pop()
        with self.assertRaises(ValueError):
            make_funky_patch(self.rom,self.config,self.font)

    def test_unsupported_accent_rejected(self):
        self.config["messages"][0]["lines"][0]="E aí!"
        with self.assertRaisesRegex(ValueError,"Unsupported"):
            make_funky_patch(self.rom,self.config,self.font)


if __name__=="__main__":
    unittest.main()
