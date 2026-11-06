"""Build four in-place Funky messages using the existing Candy dialogue font."""
from generate_ptbr_candy_pilot import make_dialogue_patch


def make_funky_patch(rom: bytes, config: dict, font_config: dict) -> tuple[list[tuple[int,bytes]],dict]:
    if rom[0x3c036c:0x3c0374]!=bytes.fromhex("74 30 96 30 d9 30 25 31"):
        raise ValueError("Funky message pointer guard failed")
    expected={(0x3c3074,34),(0x3c3096,67),(0x3c30d9,76),(0x3c3125,54)}
    actual=[(int(m["offset"],16),m["bytes"]) for m in config["messages"]]
    if len(actual)!=4 or set(actual)!=expected:
        raise ValueError("Funky message ranges must match the four identified records")
    merged={key:font_config[key] for key in ("font_offset","font_first_code","accent_slots")}
    merged["messages"]=config["messages"]
    changes,info=make_dialogue_patch(rom,merged,include_glyphs=False)
    info["uses_shared_candy_glyphs"]=True
    return changes,info
