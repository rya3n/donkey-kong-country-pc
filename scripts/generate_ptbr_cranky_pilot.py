"""Build all Cranky dialogues and identified hints using the shared Rev 1 font."""
from generate_ptbr_candy_pilot import make_dialogue_patch


def make_cranky_patch(rom: bytes, config: dict, font_config: dict) -> tuple[list[tuple[int,bytes]],dict]:
    if rom[0x3c0000:0x3c0018]!=bytes.fromhex("c4 00 04 01 30 00 7a 00 84 01 e4 01 44 02 84 02 c4 02 04 03 44 01 64 01"):
        raise ValueError("Cranky master table guard failed")
    if rom[0x3c0030:0x3c007a]!=bytes.fromhex("76 25 b0 25 e9 25 0c 26 51 26 8a 26 d7 26 08 27 48 27 9a 27 ca 27 f1 27 2a 28 77 28 bf 28 0e 29 5f 29 93 29 e1 29 18 2a 4d 2a a3 2a d0 2a 08 2b 30 2b 5b 2b 89 2b ba 2b e3 2b 31 2c 65 2c b9 2c eb 2c 3c 2d 6c 2d be 2d ee 2d"):
        raise ValueError("Cranky rant pointer guard failed")
    if rom[0x3c00c4:0x3c0104]!=bytes.fromhex("90 09 bd 09 e8 09 14 0a 4d 0a 76 0a b0 0a db 0a 00 0b 33 0b 64 0b 92 0b bf 0b dd 0b ff 0b 2c 0c 7d 0c 47 0c a1 0c d5 0c 10 0d 3e 0d 6c 0d ba 0d eb 0d 20 0e 48 0e 74 0e b0 0e cf 0e 0b 0f 10 0d"):
        raise ValueError("Cranky greeting pointer guard failed")
    if rom[0x3c0144:0x3c0164]!=bytes.fromhex("3b 2e 81 2e d6 2e 1c 2f 3c 2f 50 2f 6e 2f 9d 2f b8 2f e7 2f 1e 30 3b 2e 81 2e d6 2e 6e 2f e7 2f"):
        raise ValueError("Cranky revisit pointer guard failed")
    if rom[0x3c0244:0x3c0284]!=bytes.fromhex("34 16 88 16 c7 16 05 17 42 17 96 17 d5 17 23 18 70 18 c4 18 0f 19 63 19 b9 19 05 1a 33 1a 7c 1a ca 1a 1c 1b 6d 1b c1 1b fd 1b 49 1c 9f 1c ee 1c 30 1d 66 1d 9b 1d f4 1d 43 1e 82 1e d0 1e d0 1e"):
        raise ValueError("Cranky general tip pointer guard failed")
    if rom[0x3c02c4:0x3c0304]!=bytes.fromhex("3c 1f 4e 1f 72 1f 99 1f c5 1f f3 1f 2a 20 5e 20 91 20 ba 20 f2 20 2f 21 76 21 b0 21 d2 21 f5 21 2c 22 48 22 6f 22 b4 22 d7 22 fc 22 2d 23 7c 23 c2 23 0e 24 52 24 a4 24 f4 24 3c 25 5c 25 5c 25"):
        raise ValueError("Cranky farewell pointer guard failed")
    if rom[0x3c03a8:0x3c03c8]!=bytes.fromhex("c8 03 12 04 5f 04 9d 04 b7 04 f6 04 41 05 89 05 a6 05 d7 05 11 06 52 06 98 06 dc 06 1e 07 65 07"):
        raise ValueError("Cranky ending speech pointer guard failed")
    expected={(0x3c03c8,74),(0x3c0412,77),(0x3c045f,62),(0x3c049d,26),(0x3c04b7,63),(0x3c04f6,75),(0x3c0541,72),(0x3c0589,29),(0x3c05a6,49),(0x3c05d7,58),(0x3c0611,65),(0x3c0652,70),(0x3c0698,68),(0x3c06dc,66),(0x3c071e,71),(0x3c0765,63),(0x3c07a4,28),(0x3c07c0,50),(0x3c07f2,51),(0x3c0825,52),(0x3c0859,43),(0x3c0884,47),(0x3c08b3,56),(0x3c08eb,74),(0x3c0935,27),(0x3c0950,64),(0x3c0990,45),(0x3c09bd,43),(0x3c09e8,44),(0x3c0a14,57),(0x3c0a4d,41),(0x3c0a76,58),(0x3c0ab0,43),(0x3c0adb,37),(0x3c0b00,51),(0x3c0b33,49),(0x3c0b64,46),(0x3c0b92,45),(0x3c0bbf,30),(0x3c0bdd,34),(0x3c0bff,45),(0x3c0c2c,27),(0x3c0c47,54),(0x3c0c7d,36),(0x3c0ca1,52),(0x3c0cd5,59),(0x3c0d10,46),(0x3c0d3e,46),(0x3c0d6c,78),(0x3c0dba,49),(0x3c0deb,53),(0x3c0e20,40),(0x3c0e48,44),(0x3c0e74,60),(0x3c0eb0,31),(0x3c0ecf,60),(0x3c0f0b,42),(0x3c1634,84),(0x3c1688,63),(0x3c16c7,62),(0x3c1705,61),(0x3c1742,84),(0x3c1796,63),(0x3c17d5,78),(0x3c1823,77),(0x3c1870,84),(0x3c18c4,75),(0x3c190f,84),(0x3c1963,86),(0x3c19b9,76),(0x3c1a05,46),(0x3c1a33,73),(0x3c1a7c,78),(0x3c1aca,82),(0x3c1b1c,81),(0x3c1b6d,84),(0x3c1bc1,60),(0x3c1bfd,76),(0x3c1c49,86),(0x3c1c9f,79),(0x3c1cee,66),(0x3c1d30,54),(0x3c1d66,53),(0x3c1d9b,89),(0x3c1df4,79),(0x3c1e43,63),(0x3c1e82,78),(0x3c1ed0,63),(0x3c1f0f,45),(0x3c1f3c,18),(0x3c1f4e,36),(0x3c1f72,39),(0x3c1f99,44),(0x3c1fc5,46),(0x3c1ff3,55),(0x3c202a,52),(0x3c205e,51),(0x3c2091,41),(0x3c20ba,56),(0x3c20f2,61),(0x3c212f,71),(0x3c2176,58),(0x3c21b0,34),(0x3c21d2,35),(0x3c21f5,55),(0x3c222c,28),(0x3c2248,39),(0x3c226f,69),(0x3c22b4,35),(0x3c22d7,37),(0x3c22fc,49),(0x3c232d,79),(0x3c237c,38),(0x3c23a2,32),(0x3c23c2,76),(0x3c240e,68),(0x3c2452,82),(0x3c24a4,80),(0x3c24f4,72),(0x3c253c,32),(0x3c255c,26),(0x3c2576,58),(0x3c25b0,57),(0x3c25e9,35),(0x3c260c,69),(0x3c2651,57),(0x3c268a,77),(0x3c26d7,49),(0x3c2708,64),(0x3c2748,82),(0x3c279a,48),(0x3c27ca,39),(0x3c27f1,57),(0x3c282a,77),(0x3c2877,72),(0x3c28bf,79),(0x3c290e,81),(0x3c295f,52),(0x3c2993,78),(0x3c29e1,55),(0x3c2a18,53),(0x3c2a4d,86),(0x3c2aa3,45),(0x3c2ad0,56),(0x3c2b08,40),(0x3c2b30,43),(0x3c2b5b,46),(0x3c2b89,49),(0x3c2bba,41),(0x3c2be3,78),(0x3c2c31,52),(0x3c2c65,84),(0x3c2cb9,50),(0x3c2ceb,81),(0x3c2d3c,48),(0x3c2d6c,82),(0x3c2dbe,48),(0x3c2dee,77),(0x3c2e3b,70),(0x3c2e81,85),(0x3c2ed6,70),(0x3c2f1c,32),(0x3c2f3c,20),(0x3c2f50,30),(0x3c2f6e,47),(0x3c2f9d,27),(0x3c2fb8,47),(0x3c2fe7,55),(0x3c301e,86)}
    actual=[(int(m["offset"],16),m["bytes"]) for m in config["messages"]]
    if len(actual)!=169 or set(actual)!=expected:
        raise ValueError("Cranky ranges must match all 169 identified messages")
    for m in config["messages"]:
        offset=int(m["offset"],16)
        expected_group=("endings" if offset<0x3c07a4 else
                        "greetings" if offset<0x3c0f35 else
                        "general_tips" if offset<0x3c1f3c else
                        "farewells" if offset<0x3c2576 else
                        "rants" if offset<0x3c2e3b else
                        "revisits")
        if m.get("group")!=expected_group:
            raise ValueError("Cranky message group does not match its record")
    merged={key:font_config[key] for key in ("font_offset","font_first_code","accent_slots")}
    merged["messages"]=config["messages"]
    changes,info=make_dialogue_patch(rom,merged,include_glyphs=False)
    info["uses_shared_dialogue_glyphs"]=True
    info["complete_cranky_translation"]=True
    return changes,info


def make_cranky_tips_patch(rom: bytes, config: dict, font_config: dict) -> tuple[list[tuple[int,bytes]],dict]:
    # Identified eight-entry groups of the exact Rev 1 English hint table.
    if rom[0x3c0184:0x3c0194]!=bytes.fromhex("35 0f 72 0f b8 0f fc 0f 2e 10 35 0f b8 0f 2e 10"):
        raise ValueError("Cranky Kongo Jungle hint pointer guard failed")
    if rom[0x3c0194:0x3c01a4]!=bytes.fromhex("74 10 a6 10 d9 10 15 11 74 10 a6 10 d9 10 15 11"):
        raise ValueError("Cranky Monkey Mines hint pointer guard failed")
    if rom[0x3c01a4:0x3c01b4]!=bytes.fromhex("5b 11 b0 11 ff 11 44 12 88 12 5b 11 b0 11 ff 11"):
        raise ValueError("Cranky Gorilla Glacier hint pointer guard failed")
    if rom[0x3c01b4:0x3c01c4]!=bytes.fromhex("d4 12 19 13 55 13 95 13 e7 13 55 13 95 13 e7 13"):
        raise ValueError("Cranky Kremkroc Industries hint pointer guard failed")
    if rom[0x3c01c4:0x3c01d4]!=bytes.fromhex("35 14 61 14 9d 14 d2 14 1f 15 61 14 9d 14 d2 14"):
        raise ValueError("Cranky Chimp Caverns hint pointer guard failed")
    if rom[0x3c01d4:0x3c01e4]!=bytes.fromhex("65 15 b3 15 ef 15 65 15 b3 15 ef 15 65 15 b3 15"):
        raise ValueError("Cranky Vine Valley hint pointer guard failed")
    expected={0x3c0f35:(61,"Jungle Hijinxs"),0x3c0f72:(70,"Ropey Rampage"),
              0x3c0fb8:(68,"Barrel Cannon Canyon"),0x3c0ffc:(50,"Reptile Rumble"),
              0x3c102e:(70,"Coral Capers"),0x3c1074:(50,"Bouncy Bonanza"),
              0x3c10a6:(51,"Stop & Go Station"),0x3c10d9:(60,"Mine Cart Carnage"),
              0x3c1115:(70,"Millstone Mayhem"),0x3c1565:(78,"Orang-utan Gang"),
              0x3c15b3:(60,"Tree Top Town"),0x3c15ef:(69,"Temple Tempest"),
              0x3c115b:(85,"Snow Barrel Blast"),0x3c11b0:(79,"Croctopus Chase"),
              0x3c11ff:(69,"Ice Age Alley"),0x3c1244:(68,"Slipslide Ride"),
              0x3c1288:(76,"Torchlight Trouble"),0x3c12d4:(69,"Elevator Antics"),
              0x3c1319:(60,"Trick Track Trek"),0x3c1355:(64,"Mine Cart Madness"),
              0x3c1395:(82,"Poison Pond"),0x3c13e7:(78,"Blackout Basement"),
              0x3c1435:(44,"Manic Mincers"),0x3c1461:(60,"Misty Mine"),
              0x3c149d:(53,"Loopy Lights"),0x3c14d2:(77,"Platform Perils"),
              0x3c151f:(70,"Tanked Up Trouble")}
    actual=[(int(m["offset"],16),m["bytes"],m["stage"]) for m in config["messages"]]
    if len(actual)!=27 or set(actual)!={(offset,*spec) for offset,spec in expected.items()}:
        raise ValueError("Cranky hint ranges and stage contexts must match the twenty-seven identified records")
    for m in config["messages"]:
        offset=int(m["offset"],16)
        expected_world=("kongo-jungle" if offset<0x3c1074 else
                        "monkey-mines" if offset<0x3c115b else
                        "gorilla-glacier" if offset<0x3c12d4 else
                        "kremkroc-industries" if offset<0x3c1435 else
                        "chimp-caverns" if offset<0x3c1565 else
                        "vine-valley")
        if m.get("world")!=expected_world:
            raise ValueError("Cranky hint world context does not match its record")
    merged={key:font_config[key] for key in ("font_offset","font_first_code","accent_slots")}
    merged["messages"]=config["messages"]
    changes,info=make_dialogue_patch(rom,merged,include_glyphs=False)
    info["uses_shared_dialogue_glyphs"]=True
    info["stages"]=[m["stage"] for m in config["messages"]]
    info["complete_cranky_translation"]=True
    return changes,info
