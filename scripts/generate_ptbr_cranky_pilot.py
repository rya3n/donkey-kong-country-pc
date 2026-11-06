"""Build Cranky greetings and identified hints using the shared Rev 1 font."""
from generate_ptbr_candy_pilot import make_dialogue_patch


def make_cranky_patch(rom: bytes, config: dict, font_config: dict) -> tuple[list[tuple[int,bytes]],dict]:
    if rom[0x3c0000:0x3c0004]!=bytes.fromhex("c4 00 04 01"):
        raise ValueError("Cranky greeting table guard failed")
    if rom[0x3c00c4:0x3c00cc]!=bytes.fromhex("90 09 bd 09 e8 09 14 0a"):
        raise ValueError("Cranky greeting pointer guard failed")
    expected={(0x3c07a4,28),(0x3c0935,27),(0x3c0990,45),
              (0x3c09bd,43),(0x3c09e8,44),(0x3c0a14,57)}
    actual=[(int(m["offset"],16),m["bytes"]) for m in config["messages"]]
    if len(actual)!=6 or set(actual)!=expected:
        raise ValueError("Cranky ranges must match the six identified greetings")
    merged={key:font_config[key] for key in ("font_offset","font_first_code","accent_slots")}
    merged["messages"]=config["messages"]
    changes,info=make_dialogue_patch(rom,merged,include_glyphs=False)
    info["uses_shared_dialogue_glyphs"]=True
    info["complete_cranky_translation"]=False
    return changes,info


def make_cranky_tips_patch(rom: bytes, config: dict, font_config: dict) -> tuple[list[tuple[int,bytes]],dict]:
    # First two eight-entry groups of the exact Rev 1 English hint table.
    if rom[0x3c0184:0x3c0194]!=bytes.fromhex("35 0f 72 0f b8 0f fc 0f 2e 10 35 0f b8 0f 2e 10"):
        raise ValueError("Cranky Kongo Jungle hint pointer guard failed")
    if rom[0x3c0194:0x3c01a4]!=bytes.fromhex("74 10 a6 10 d9 10 15 11 74 10 a6 10 d9 10 15 11"):
        raise ValueError("Cranky Monkey Mines hint pointer guard failed")
    expected={0x3c0f35:(61,"Jungle Hijinxs"),0x3c0f72:(70,"Ropey Rampage"),
              0x3c0fb8:(68,"Barrel Cannon Canyon"),0x3c0ffc:(50,"Reptile Rumble"),
              0x3c102e:(70,"Coral Capers"),0x3c1074:(50,"Bouncy Bonanza"),
              0x3c10a6:(51,"Stop & Go Station"),0x3c10d9:(60,"Mine Cart Carnage"),
              0x3c1115:(70,"Millstone Mayhem")}
    actual=[(int(m["offset"],16),m["bytes"],m["stage"]) for m in config["messages"]]
    if len(actual)!=9 or set(actual)!={(offset,*spec) for offset,spec in expected.items()}:
        raise ValueError("Cranky hint ranges and stage contexts must match the nine identified records")
    for m in config["messages"]:
        expected_world="kongo-jungle" if int(m["offset"],16)<0x3c1074 else "monkey-mines"
        if m.get("world")!=expected_world:
            raise ValueError("Cranky hint world context does not match its record")
    merged={key:font_config[key] for key in ("font_offset","font_first_code","accent_slots")}
    merged["messages"]=config["messages"]
    changes,info=make_dialogue_patch(rom,merged,include_glyphs=False)
    info["uses_shared_dialogue_glyphs"]=True
    info["stages"]=[m["stage"] for m in config["messages"]]
    info["complete_cranky_translation"]=False
    return changes,info
