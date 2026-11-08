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
                     0x3c0ffc:[27,22],0x3c102e:[28,25,16],0x3c1074:[19,12,18],
                     0x3c10a6:[14,17,19],0x3c10d9:[23,14,22],0x3c1115:[24,25,20],
                     0x3c1565:[30,28,19],0x3c15b3:[15,19,25],0x3c15ef:[28,22,18],
                     0x3c115b:[30,27,27],0x3c11b0:[29,25,24],0x3c11ff:[17,24,27],
                     0x3c1244:[25,27,15],0x3c1288:[29,24,22],
                     0x3c12d4:[27,20,21],0x3c1319:[29,16,14],0x3c1355:[21,21,21],
                     0x3c1395:[25,26,30],0x3c13e7:[28,26,23],
                     0x3c1435:[26,17],0x3c1461:[20,21,18],0x3c149d:[26,26],
                     0x3c14d2:[27,27,22],0x3c151f:[27,23,19]}
        rom=bytearray(4194304)
        rom[0xee62:0xee6f]=bytes.fromhex("a2 e9 00 a9 dc d6 a0 00 06 22 ad 99 b9")
        rom[0x3c0184:0x3c0194]=bytes.fromhex("35 0f 72 0f b8 0f fc 0f 2e 10 35 0f b8 0f 2e 10")
        rom[0x3c0194:0x3c01a4]=bytes.fromhex("74 10 a6 10 d9 10 15 11 74 10 a6 10 d9 10 15 11")
        rom[0x3c01a4:0x3c01b4]=bytes.fromhex("5b 11 b0 11 ff 11 44 12 88 12 5b 11 b0 11 ff 11")
        rom[0x3c01b4:0x3c01c4]=bytes.fromhex("d4 12 19 13 55 13 95 13 e7 13 55 13 95 13 e7 13")
        rom[0x3c01c4:0x3c01d4]=bytes.fromhex("35 14 61 14 9d 14 d2 14 1f 15 61 14 9d 14 d2 14")
        rom[0x3c01d4:0x3c01e4]=bytes.fromhex("65 15 b3 15 ef 15 65 15 b3 15 ef 15 65 15 b3 15")
        stage_lines=[0,1,2,1,2,2,1,0,2,0,2,2,0,0,0,2,2,0,0,0,0,0,1,2,0,0,0]
        for i,m in enumerate(self.config["messages"]):
            offset=int(m["offset"],16);widths=self.widths[offset]
            lines=["X"*n for n in widths]
            slot=stage_lines[i];lines[slot]=m["stage"].ljust(widths[slot])
            if i==2: lines[1]="Winky".ljust(widths[1])
            if i==4: lines[0]="Croctopus".ljust(widths[0])
            if i==16: lines[0]="TNT".ljust(widths[0])
            if i==18: lines[1]="Gnawty".ljust(widths[1])
            if i==22: lines[0]="Diddy TNT".ljust(widths[0])
            rom[offset:offset+m["bytes"]]=encode_message(lines,{},max(29,m["max_line"]))
        self.rom=bytes(rom)

    def test_exact_records_line_counts_and_parities(self):
        patches,info=make_cranky_tips_patch(self.rom,self.config,self.font)
        self.assertEqual([(o,len(b)) for o,b in patches],list(zip(self.widths,[61,70,68,50,70,50,51,60,70,78,60,69,85,79,69,68,76,69,60,64,82,78,44,60,53,77,70])))
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
        for index,name in ((2,"Winky"),(4,"Croctopus"),(18,"Gnawty"),(22,"Diddy")):
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

    def test_wrong_world_cannot_mislabel_a_hint(self):
        self.config["messages"][5]["world"]="kongo-jungle"
        with self.assertRaisesRegex(ValueError,"world context"):
            make_cranky_tips_patch(self.rom,self.config,self.font)

    def test_changed_monkey_mines_pointer_is_rejected(self):
        rom=bytearray(self.rom);rom[0x3c0194]^=1
        with self.assertRaisesRegex(ValueError,"Monkey Mines hint pointer"):
            make_cranky_tips_patch(bytes(rom),self.config,self.font)

    def test_changed_vine_valley_pointer_is_rejected(self):
        rom=bytearray(self.rom);rom[0x3c01d4]^=1
        with self.assertRaisesRegex(ValueError,"Vine Valley hint pointer"):
            make_cranky_tips_patch(bytes(rom),self.config,self.font)

    def test_changed_gorilla_glacier_pointer_is_rejected(self):
        rom=bytearray(self.rom);rom[0x3c01a4]^=1
        with self.assertRaisesRegex(ValueError,"Gorilla Glacier hint pointer"):
            make_cranky_tips_patch(bytes(rom),self.config,self.font)

    def test_changed_kremkroc_industries_pointer_is_rejected(self):
        rom=bytearray(self.rom);rom[0x3c01b4]^=1
        with self.assertRaisesRegex(ValueError,"Kremkroc Industries hint pointer"):
            make_cranky_tips_patch(bytes(rom),self.config,self.font)

    def test_changed_chimp_caverns_pointer_is_rejected(self):
        rom=bytearray(self.rom);rom[0x3c01c4]^=1
        with self.assertRaisesRegex(ValueError,"Chimp Caverns hint pointer"):
            make_cranky_tips_patch(bytes(rom),self.config,self.font)


if __name__=="__main__":
    unittest.main()
