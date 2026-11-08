"""Build all thirteen in-place Funky messages using the existing Candy dialogue font."""
from generate_ptbr_candy_pilot import make_dialogue_patch


def make_funky_patch(rom: bytes, config: dict, font_config: dict) -> tuple[list[tuple[int,bytes]],dict]:
    if rom[0x3c036c:0x3c038c]!=bytes.fromhex("74 30 96 30 d9 30 25 31 34 33 7e 33 ca 33 01 34 40 34 34 33 7e 33 ca 33 95 34 d9 34 2e 35 75 35"):
        raise ValueError("Funky message pointer guard failed")
    expected={
        0x3c3074:(34,"opening"),0x3c3096:(67,"opening"),0x3c30d9:(76,"opening"),0x3c3125:(54,"opening"),
        0x3c3334:(74,"revisits"),0x3c337e:(76,"revisits"),0x3c33ca:(55,"revisits"),0x3c3401:(63,"revisits"),
        0x3c3440:(85,"revisits"),0x3c3495:(68,"revisits"),0x3c34d9:(85,"revisits"),0x3c352e:(71,"revisits"),
        0x3c3575:(85,"revisits"),
    }
    actual=[(int(m["offset"],16),m["bytes"],m.get("group")) for m in config["messages"]]
    if len(actual)!=len(expected) or {o:(b,g) for o,b,g in actual}!=expected:
        raise ValueError("Funky message ranges must match the thirteen identified records")
    merged={key:font_config[key] for key in ("font_offset","font_first_code","accent_slots")}
    merged["messages"]=config["messages"]
    changes,info=make_dialogue_patch(rom,merged,include_glyphs=False)
    info["uses_shared_candy_glyphs"]=True
    info["complete_funky_translation"]=True
    return changes,info
