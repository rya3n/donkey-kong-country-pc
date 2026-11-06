"""Build six Cranky greetings using the shared Rev 1 dialogue font."""
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
