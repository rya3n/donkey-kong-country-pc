"""Cranky complete dialogue boundaries, groups and names, with synthetic source records."""
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
        self.widths={0x3c03c8:[24, 26, 23],0x3c0412:[26, 21, 29],0x3c045f:[26, 17, 18],0x3c049d:[25],0x3c04b7:[24, 18, 20],0x3c04f6:[24, 26, 24],0x3c0541:[24, 23, 24],0x3c0589:[28],0x3c05a6:[22, 26],0x3c05d7:[27, 30],0x3c0611:[22, 14, 28],0x3c0652:[20, 25, 24],0x3c0698:[23, 19, 25],0x3c06dc:[24, 22, 19],0x3c071e:[23, 22, 25],0x3c0765:[21, 22, 19],0x3c07a4:[27],0x3c07c0:[17, 15, 17],0x3c07f2:[21, 29],0x3c0825:[27, 24],0x3c0859:[18, 24],0x3c0884:[25, 21],0x3c08b3:[19, 16, 20],0x3c08eb:[23, 28, 22],0x3c0935:[26],0x3c0950:[21, 20, 22],0x3c0990:[20, 24],0x3c09bd:[24, 18],0x3c09e8:[25, 18],0x3c0a14:[24, 11, 21],0x3c0a4d:[11, 29],0x3c0a76:[29, 28],0x3c0ab0:[21, 21],0x3c0adb:[14, 22],0x3c0b00:[27, 23],0x3c0b33:[21, 27],0x3c0b64:[20, 25],0x3c0b92:[18, 26],0x3c0bbf:[29],0x3c0bdd:[18, 15],0x3c0bff:[24, 20],0x3c0c2c:[26],0x3c0c47:[25, 28],0x3c0c7d:[8, 27],0x3c0ca1:[12, 23, 16],0x3c0cd5:[17, 25, 16],0x3c0d10:[19, 26],0x3c0d3e:[29, 16],0x3c0d6c:[29, 21, 27],0x3c0dba:[19, 29],0x3c0deb:[18, 15, 19],0x3c0e20:[18, 21],0x3c0e48:[25, 18],0x3c0e74:[29, 30],0x3c0eb0:[30],0x3c0ecf:[18, 24, 17],0x3c0f0b:[16, 25],0x3c1634:[25, 30, 28],0x3c1688:[20, 24, 18],0x3c16c7:[22, 13, 26],0x3c1705:[29, 14, 17],0x3c1742:[22, 30, 31],0x3c1796:[27, 23, 12],0x3c17d5:[29, 28, 20],0x3c1823:[29, 27, 20],0x3c1870:[30, 25, 28],0x3c18c4:[28, 25, 21],0x3c190f:[29, 29, 25],0x3c1963:[25, 30, 30],0x3c19b9:[24, 27, 24],0x3c1a05:[22, 23],0x3c1a33:[27, 19, 26],0x3c1a7c:[28, 30, 19],0x3c1aca:[27, 25, 29],0x3c1b1c:[24, 29, 27],0x3c1b6d:[28, 28, 27],0x3c1bc1:[8, 28, 23],0x3c1bfd:[28, 23, 24],0x3c1c49:[29, 29, 27],0x3c1c9f:[29, 25, 24],0x3c1cee:[22, 29, 14],0x3c1d30:[27, 26],0x3c1d66:[26, 26],0x3c1d9b:[30, 27, 31],0x3c1df4:[28, 29, 21],0x3c1e43:[25, 19, 18],0x3c1e82:[28, 24, 25],0x3c1ed0:[25, 18, 19],0x3c1f0f:[21, 23],0x3c1f3c:[17],0x3c1f4e:[20, 15],0x3c1f72:[21, 17],0x3c1f99:[30, 13],0x3c1fc5:[21, 24],0x3c1ff3:[26, 28],0x3c202a:[17, 15, 19],0x3c205e:[25, 25],0x3c2091:[18, 22],0x3c20ba:[25, 15, 15],0x3c20f2:[26, 22, 12],0x3c212f:[25, 22, 23],0x3c2176:[15, 26, 16],0x3c21b0:[18, 15],0x3c21d2:[22, 12],0x3c21f5:[28, 26],0x3c222c:[27],0x3c2248:[17, 21],0x3c226f:[25, 18, 25],0x3c22b4:[14, 20],0x3c22d7:[19, 17],0x3c22fc:[25, 23],0x3c232d:[27, 24, 27],0x3c237c:[18, 19],0x3c23a2:[31],0x3c23c2:[21, 27, 27],0x3c240e:[24, 23, 20],0x3c2452:[24, 27, 30],0x3c24a4:[29, 28, 22],0x3c24f4:[26, 16, 29],0x3c253c:[24, 7],0x3c255c:[25],0x3c2576:[15, 18, 24],0x3c25b0:[21, 9, 26],0x3c25e9:[18, 16],0x3c260c:[17, 24, 27],0x3c2651:[20, 24, 12],0x3c268a:[29, 21, 26],0x3c26d7:[26, 22],0x3c2708:[21, 19, 23],0x3c2748:[24, 27, 30],0x3c279a:[28, 19],0x3c27ca:[21, 17],0x3c27f1:[30, 26],0x3c282a:[25, 24, 27],0x3c2877:[23, 27, 21],0x3c28bf:[26, 27, 25],0x3c290e:[26, 24, 30],0x3c295f:[26, 25],0x3c2993:[27, 27, 23],0x3c29e1:[26, 28],0x3c2a18:[22, 30],0x3c2a4d:[30, 28, 27],0x3c2aa3:[29, 15],0x3c2ad0:[19, 21, 15],0x3c2b08:[22, 17],0x3c2b30:[24, 18],0x3c2b5b:[28, 17],0x3c2b89:[27, 21],0x3c2bba:[20, 20],0x3c2be3:[29, 29, 19],0x3c2c31:[21, 30],0x3c2c65:[28, 24, 31],0x3c2cb9:[27, 22],0x3c2ceb:[27, 24, 29],0x3c2d3c:[29, 18],0x3c2d6c:[22, 29, 30],0x3c2dbe:[23, 24],0x3c2dee:[26, 20, 30],0x3c2e3b:[21, 26, 22],0x3c2e81:[26, 29, 29],0x3c2ed6:[16, 25, 28],0x3c2f1c:[11, 20],0x3c2f3c:[19],0x3c2f50:[29],0x3c2f6e:[23, 23],0x3c2f9d:[26],0x3c2fb8:[28, 18],0x3c2fe7:[5, 29, 20],0x3c301e:[25, 29, 31]}
        rom=bytearray(4194304)
        rom[0xee62:0xee6f]=bytes.fromhex("a2 e9 00 a9 dc d6 a0 00 06 22 ad 99 b9")
        rom[0x3c0000:0x3c0018]=bytes.fromhex("c4 00 04 01 30 00 7a 00 84 01 e4 01 44 02 84 02 c4 02 04 03 44 01 64 01")
        rom[0x3c0030:0x3c007a]=bytes.fromhex("76 25 b0 25 e9 25 0c 26 51 26 8a 26 d7 26 08 27 48 27 9a 27 ca 27 f1 27 2a 28 77 28 bf 28 0e 29 5f 29 93 29 e1 29 18 2a 4d 2a a3 2a d0 2a 08 2b 30 2b 5b 2b 89 2b ba 2b e3 2b 31 2c 65 2c b9 2c eb 2c 3c 2d 6c 2d be 2d ee 2d")
        rom[0x3c00c4:0x3c0104]=bytes.fromhex("90 09 bd 09 e8 09 14 0a 4d 0a 76 0a b0 0a db 0a 00 0b 33 0b 64 0b 92 0b bf 0b dd 0b ff 0b 2c 0c 7d 0c 47 0c a1 0c d5 0c 10 0d 3e 0d 6c 0d ba 0d eb 0d 20 0e 48 0e 74 0e b0 0e cf 0e 0b 0f 10 0d")
        rom[0x3c0144:0x3c0164]=bytes.fromhex("3b 2e 81 2e d6 2e 1c 2f 3c 2f 50 2f 6e 2f 9d 2f b8 2f e7 2f 1e 30 3b 2e 81 2e d6 2e 6e 2f e7 2f")
        rom[0x3c0244:0x3c0284]=bytes.fromhex("34 16 88 16 c7 16 05 17 42 17 96 17 d5 17 23 18 70 18 c4 18 0f 19 63 19 b9 19 05 1a 33 1a 7c 1a ca 1a 1c 1b 6d 1b c1 1b fd 1b 49 1c 9f 1c ee 1c 30 1d 66 1d 9b 1d f4 1d 43 1e 82 1e d0 1e d0 1e")
        rom[0x3c02c4:0x3c0304]=bytes.fromhex("3c 1f 4e 1f 72 1f 99 1f c5 1f f3 1f 2a 20 5e 20 91 20 ba 20 f2 20 2f 21 76 21 b0 21 d2 21 f5 21 2c 22 48 22 6f 22 b4 22 d7 22 fc 22 2d 23 7c 23 c2 23 0e 24 52 24 a4 24 f4 24 3c 25 5c 25 5c 25")
        rom[0x3c03a8:0x3c03c8]=bytes.fromhex("c8 03 12 04 5f 04 9d 04 b7 04 f6 04 41 05 89 05 a6 05 d7 05 11 06 52 06 98 06 dc 06 1e 07 65 07")
        names={0x3c03c8:'Donkey',0x3c0412:'Kremlings',0x3c049d:'Red Team',0x3c04f6:'Yellow Team',0x3c0541:'Red Team',0x3c0589:'Yellow Team',0x3c0611:'Kremlings Donkey',0x3c0698:'Red Team',0x3c06dc:'Yellow Team',0x3c071e:'Yellow Team',0x3c0765:'Red Team',0x3c07a4:'Donkey Diddy',0x3c07c0:'Donkey',0x3c07f2:'Donkey',0x3c0935:'Donks Diddy',0x3c0950:'Diddy',0x3c0a14:'Funky Kong',0x3c0bff:'Kremlings',0x3c0d6c:'Kremlings',0x3c0deb:'KONG',0x3c1634:'Rambi',0x3c1688:'Expresso',0x3c16c7:'Enguarde',0x3c1705:'Rambi',0x3c1823:'Rambi',0x3c1963:'Expresso',0x3c1a05:'Candy',0x3c1a33:'Funky',0x3c1b1c:'Kremlings',0x3c1b6d:'DK',0x3c1bfd:'Klaptrap',0x3c1c49:'Zingers Winky',0x3c1c9f:'Klump',0x3c1cee:'Kremling Krusha',0x3c1ed0:'Slippa',0x3c1f0f:'Gnawty',0x3c205e:'Cranky',0x3c22fc:'Donkey',0x3c23c2:'Donkey Kong',0x3c2ad0:'D.K.Country',0x3c2dee:'Game & Watch'}
        for m in self.config["messages"]:
            offset=int(m["offset"],16)
            lines=["X"*n for n in self.widths[offset]]
            if offset in names:
                idx=max(range(len(lines)),key=lambda i:self.widths[offset][i])
                lines[idx]=names[offset].ljust(self.widths[offset][idx])
            rom[offset:offset+m["bytes"]]=encode_message(lines,{},max(29,m["max_line"]))
        self.rom=bytes(rom)

    def test_exact_ranges_and_native_line_parities(self):
        patches,info=make_cranky_patch(self.rom,self.config,self.font)
        self.assertEqual([(o,len(b)) for o,b in patches],[(int(m["offset"],16),m["bytes"]) for m in self.config["messages"]])
        self.assertTrue(info["complete_cranky_translation"])
        for m in self.config["messages"]:
            fitted=fitted_lines(m,self.widths[int(m["offset"],16)])
            self.assertEqual([s.strip() for s in fitted],m["lines"])
            self.assertEqual([len(s)%2 for s in fitted],[n%2 for n in self.widths[int(m["offset"],16)]])

    def test_donks_nickname_is_preserved(self):
        msg=next(m for m in self.config["messages"] if m["offset"]=="0x3C0935")
        msg["lines"]=["Ei, Diddy! Cadê o Donkey?"]
        with self.assertRaisesRegex(ValueError,"Protected name"):
            make_cranky_patch(self.rom,self.config,self.font)

    def test_other_character_name_is_preserved(self):
        msg=next(m for m in self.config["messages"] if m["offset"]=="0x3C0A14")
        msg["lines"][-1]="Aquele irritante?"
        with self.assertRaisesRegex(ValueError,"Protected name"):
            make_cranky_patch(self.rom,self.config,self.font)

    def test_moved_message_is_rejected(self):
        self.config["messages"][0]["offset"]="0x3C03C9"
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
        self.config["messages"][-1]["group"]="greetings"
        with self.assertRaisesRegex(ValueError,"message group"):
            make_cranky_patch(self.rom,self.config,self.font)


if __name__=="__main__":
    unittest.main()
