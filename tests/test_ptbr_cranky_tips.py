"""Hint boundaries, phase identities and protected entities on synthetic data."""
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from generate_ptbr_candy_pilot import encode_message, fitted_lines
from generate_ptbr_cranky_pilot import make_cranky_tips_patch


class CrankyTipsTests(unittest.TestCase):
    def setUp(self):
        self.config=json.loads((ROOT/"localization/pt-BR/cranky-tips-pilot.json").read_text(encoding="utf-8"))
        self.font=json.loads((ROOT/"localization/pt-BR/candy-pilot.json").read_text(encoding="utf-8"))
        self.widths={0x3c0f35:[18,22,20],0x3c0f72:[23,21,25],0x3c0fb8:[22,25,20],
                     0x3c0ffc:[27,22],0x3c102e:[28,25,16]}
        rom=bytearray(4194304)
        rom[0xee62:0xee6f]=bytes.fromhex("a2 e9 00 a9 dc d6 a0 00 06 22 ad 99 b9")
        rom[0x3c0184:0x3c0194]=bytes.fromhex("35 0f 72 0f b8 0f fc 0f 2e 10 35 0f b8 0f 2e 10")
        stage_lines=[0,1,2,1,2]
        for i,m in enumerate(self.config["messages"]):
            offset=int(m["offset"],16);widths=self.widths[offset]
            lines=["X"*n for n in widths]
            slot=stage_lines[i];lines[slot]=m["stage"].ljust(widths[slot])
            if i==2: lines[1]="Winky".ljust(widths[1])
            if i==4: lines[0]="Croctopus".ljust(widths[0])
            rom[offset:offset+m["bytes"]]=encode_message(lines,{},29)
        self.rom=bytes(rom)

    def test_exact_records_line_counts_and_parities(self):
        patches,info=make_cranky_tips_patch(self.rom,self.config,self.font)
        self.assertEqual([(o,len(b)) for o,b in patches],list(zip(self.widths,[61,70,68,50,70])))
        self.assertEqual(info["accented_glyphs"],0)
        for m in self.config["messages"]:
            widths=self.widths[int(m["offset"],16)]
            fitted=fitted_lines(m,widths)
            self.assertEqual([len(s)%2 for s in fitted],[n%2 for n in widths])
            self.assertEqual([s.strip() for s in fitted],m["lines"])
            self.assertEqual(sum(map(len,fitted)),m["bytes"]-1)

    def test_each_complete_phase_name_is_protected(self):
        for m in self.config["messages"]:
            old=m["lines"][:]
            m["lines"]=[s.replace(m["stage"],"fase") for s in old]
            with self.subTest(stage=m["stage"]),self.assertRaisesRegex(ValueError,"Protected name"):
                make_cranky_tips_patch(self.rom,self.config,self.font)
            m["lines"]=old

    def test_winky_and_croctopus_cannot_be_renamed(self):
        for index,name in ((2,"Winky"),(4,"Croctopus")):
            m=self.config["messages"][index];old=m["lines"][:]
            m["lines"]=[s.replace(name,"bicho") for s in old]
            with self.subTest(name=name),self.assertRaisesRegex(ValueError,"Protected name"):
                make_cranky_tips_patch(self.rom,self.config,self.font)
            m["lines"]=old

    def test_mismatched_phase_context_is_rejected(self):
        self.config["messages"][0]["stage"]="Ropey Rampage"
        with self.assertRaisesRegex(ValueError,"stage contexts"):
            make_cranky_tips_patch(self.rom,self.config,self.font)

    def test_changed_original_hint_pointer_is_rejected(self):
        rom=bytearray(self.rom);rom[0x3c0184]^=1
        with self.assertRaisesRegex(ValueError,"pointer guard"):
            make_cranky_tips_patch(bytes(rom),self.config,self.font)


if __name__=="__main__":
    unittest.main()
