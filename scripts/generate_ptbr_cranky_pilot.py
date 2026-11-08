"""Build Cranky greetings and identified hints using the shared Rev 1 font."""
from generate_ptbr_candy_pilot import make_dialogue_patch


def make_cranky_patch(rom: bytes, config: dict, font_config: dict) -> tuple[list[tuple[int,bytes]],dict]:
    if rom[0x3c0000:0x3c0004]!=bytes.fromhex("c4 00 04 01"):
        raise ValueError("Cranky greeting table guard failed")
    if rom[0x3c0014:0x3c0018]!=bytes.fromhex("44 01 64 01"):
        raise ValueError("Cranky revisit table guard failed")
    if rom[0x3c00c4:0x3c00cc]!=bytes.fromhex("90 09 bd 09 e8 09 14 0a"):
        raise ValueError("Cranky greeting pointer guard failed")
    if rom[0x3c0144:0x3c0164]!=bytes.fromhex("3b 2e 81 2e d6 2e 1c 2f 3c 2f 50 2f 6e 2f 9d 2f b8 2f e7 2f 1e 30 3b 2e 81 2e d6 2e 6e 2f e7 2f"):
        raise ValueError("Cranky revisit pointer guard failed")
    expected={(0x3c07a4,28),(0x3c0935,27),(0x3c0990,45),
              (0x3c09bd,43),(0x3c09e8,44),(0x3c0a14,57),
              (0x3c2e3b,70),(0x3c2e81,85),(0x3c2ed6,70),
              (0x3c2f1c,32),(0x3c2f3c,20),(0x3c2f50,30),
              (0x3c2f6e,47),(0x3c2f9d,27),(0x3c2fb8,47),
              (0x3c2fe7,55),(0x3c301e,86)}
    actual=[(int(m["offset"],16),m["bytes"]) for m in config["messages"]]
    if len(actual)!=17 or set(actual)!=expected:
        raise ValueError("Cranky ranges must match the seventeen identified greetings and revisits")
    for m in config["messages"]:
        offset=int(m["offset"],16)
        expected_group="greetings" if offset<0x3c2e3b else "revisits"
        if m.get("group")!=expected_group:
            raise ValueError("Cranky message group does not match its record")
    merged={key:font_config[key] for key in ("font_offset","font_first_code","accent_slots")}
    merged["messages"]=config["messages"]
    changes,info=make_dialogue_patch(rom,merged,include_glyphs=False)
    info["uses_shared_dialogue_glyphs"]=True
    info["complete_cranky_translation"]=False
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
    info["complete_cranky_translation"]=False
    return changes,info
