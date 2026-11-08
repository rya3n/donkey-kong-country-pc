"""Cranky first-batch boundaries and names, with synthetic source records."""
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from generate_ptbr_candy_pilot import encode_message, fitted_lines
from generate_ptbr_cranky_pilot import make_cranky_patch


class CrankyPilotTests(unittest.TestCase):
    def setUp(self):
        self.config=json.loads((ROOT/"localization/pt-BR/cranky-pilot.json").read_text(encoding="utf-8"))
        self.font=json.loads((ROOT/"localization/pt-BR/candy-pilot.json").read_text(encoding="utf-8"))
        self.widths={0x3c07a4:[27],0x3c0935:[26],0x3c0990:[20,24],
                     0x3c09bd:[24,18],0x3c09e8:[25,18],0x3c0a14:[24,11,21],
                     0x3c2e3b:[21,26,22],0x3c2e81:[26,29,29],0x3c2ed6:[16,25,28],
                     0x3c2f1c:[11,20],0x3c2f3c:[19],0x3c2f50:[29],
                     0x3c2f6e:[23,23],0x3c2f9d:[26],0x3c2fb8:[28,18],
                     0x3c2fe7:[5,29,20],0x3c301e:[25,29,31]}
        rom=bytearray(4194304)
        rom[0xee62:0xee6f]=bytes.fromhex("a2 e9 00 a9 dc d6 a0 00 06 22 ad 99 b9")
        rom[0x3c0000:0x3c0004]=bytes.fromhex("c4 00 04 01")
        rom[0x3c0014:0x3c0018]=bytes.fromhex("44 01 64 01")
        rom[0x3c00c4:0x3c00cc]=bytes.fromhex("90 09 bd 09 e8 09 14 0a")
        rom[0x3c0144:0x3c0164]=bytes.fromhex("3b 2e 81 2e d6 2e 1c 2f 3c 2f 50 2f 6e 2f 9d 2f b8 2f e7 2f 1e 30 3b 2e 81 2e d6 2e 6e 2f e7 2f")
        for m in self.config["messages"]:
            offset=int(m["offset"],16)
            lines=["X"*n for n in self.widths[offset]]
            names={0x3c07a4:"Donkey Diddy",0x3c0935:"Diddy Donks",0x3c0a14:"Funky Kong"}
            if offset in names: lines[-1]=names[offset].ljust(self.widths[offset][-1])
            rom[offset:offset+m["bytes"]]=encode_message(lines,{},max(29,m["max_line"]))
        self.rom=bytes(rom)

    def test_six_exact_ranges_and_native_line_parities(self):
        patches,info=make_cranky_patch(self.rom,self.config,self.font)
        self.assertEqual([(o,len(b)) for o,b in patches],list(zip(self.widths,[28,27,45,43,44,57,70,85,70,32,20,30,47,27,47,55,86])))
        self.assertFalse(info["complete_cranky_translation"])
        for m in self.config["messages"]:
            fitted=fitted_lines(m,self.widths[int(m["offset"],16)])
            self.assertEqual([s.strip() for s in fitted],m["lines"])
            self.assertEqual([len(s)%2 for s in fitted],[n%2 for n in self.widths[int(m["offset"],16)]])

    def test_donks_nickname_is_preserved(self):
        self.config["messages"][1]["lines"]=["Ei, Diddy! Cadê o Donkey?"]
        with self.assertRaisesRegex(ValueError,"Protected name"):
            make_cranky_patch(self.rom,self.config,self.font)

    def test_other_character_name_is_preserved(self):
        self.config["messages"][5]["lines"][-1]="Aquele irritante?"
        with self.assertRaisesRegex(ValueError,"Protected name"):
            make_cranky_patch(self.rom,self.config,self.font)

    def test_moved_message_is_rejected(self):
        self.config["messages"][0]["offset"]="0x3C07A5"
        with self.assertRaisesRegex(ValueError,"ranges"):
            make_cranky_patch(self.rom,self.config,self.font)

    def test_changed_greeting_pointer_is_rejected(self):
        rom=bytearray(self.rom);rom[0x3c00c4]^=1
        with self.assertRaisesRegex(ValueError,"pointer guard"):
            make_cranky_patch(bytes(rom),self.config,self.font)

    def test_changed_revisit_pointer_is_rejected(self):
        rom=bytearray(self.rom);rom[0x3c0144]^=1
        with self.assertRaisesRegex(ValueError,"revisit pointer guard"):
            make_cranky_patch(bytes(rom),self.config,self.font)

    def test_wrong_group_is_rejected(self):
        self.config["messages"][6]["group"]="greetings"
        with self.assertRaisesRegex(ValueError,"message group"):
            make_cranky_patch(self.rom,self.config,self.font)


if __name__=="__main__":
    unittest.main()
