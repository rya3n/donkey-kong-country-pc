"""Build in-place Candy dialogue and three lower-case accented glyphs.

The original message sizes, terminators and pointers are retained. Only unused
English character slots are reused; this is not a multilingual font extension.
"""
from __future__ import annotations
from pathlib import Path
import json
from inventory_rev1_text import decode_lines
from check_ptbr_catalog import occurrences

ROOT=Path(__file__).resolve().parents[1]


def decode_tile(data: bytes) -> list[list[int]]:
    return [[((data[y*2]>>(7-x))&1)|(((data[y*2+1]>>(7-x))&1)<<1)
             for x in range(8)] for y in range(8)]


def encode_tile(pixels: list[list[int]]) -> bytes:
    data=bytearray(16)
    for y,row in enumerate(pixels):
        for x,value in enumerate(row):
            data[y*2]|=(value&1)<<(7-x)
            data[y*2+1]|=((value>>1)&1)<<(7-x)
    return bytes(data)


def encode_message(lines: list[str], accents: dict, limit: int) -> bytes:
    data=bytearray()
    for line in lines:
        if not line.strip() or len(line)>limit:
            raise ValueError("Empty/overlong dialogue line")
        for char in line:
            if char in accents:
                code=accents[char]["code"]
            elif 0x20<=ord(char)<=0x7e:
                code=ord(char)
                if code in {item["code"] for item in accents.values()}:
                    raise ValueError("Literal collides with an accent slot")
            else:
                raise ValueError(f"Unsupported dialogue glyph: {char}")
            data.append(code)
        data[-1]|=0x80
    data.append(0)
    return bytes(data)


def make_candy_patch(rom: bytes, config: dict) -> tuple[list[tuple[int,bytes]],dict]:
    # Font DMA and first-visit text pointers independently observed in Rev 1.
    if rom[0xee62:0xee6f]!=bytes.fromhex("a2 e9 00 a9 dc d6 a0 00 06 22 ad 99 b9"):
        raise ValueError("Rev 1 dialogue-font pointer guard failed")
    if rom[0x3c0354:0x3c0358]!=bytes.fromhex("5b 31 89 31"):
        raise ValueError("Candy message pointer guard failed")
    regions=json.loads((ROOT/"localization/pt-BR/regions.json").read_text(encoding="utf-8"))["regions"]
    slots={item["code"] for item in config["accent_slots"].values()}
    if len(slots)!=len(config["accent_slots"]) or any(not 0x20<=x<=0x7e for x in slots):
        raise ValueError("Invalid accent slots")
    for region in regions:
        begin,end=int(region["start"],16),int(region["end"],16)
        if any((value&127) in slots for value in rom[begin:end]):
            raise ValueError("An English source text already uses an accent slot")
    protected=json.loads((ROOT/"localization/pt-BR/policy.json").read_text(encoding="utf-8"))
    changes=[]
    for message in config["messages"]:
        offset,size=int(message["offset"],16),message["bytes"]
        source=rom[offset:offset+size]
        if not source or source[-1]!=0 or 0 in source[:-1]:
            raise ValueError("Message boundary guard failed")
        original=" ".join(decode_lines(source[:-1]))
        target=" ".join(line.strip() for line in message["lines"])
        for term in protected["protected_terms"]+protected["context_review_terms"]:
            count=occurrences(original,term)
            if count and occurrences(target,term)<count:
                raise ValueError(f"Protected name changed: {term}")
        encoded=encode_message(message["lines"],config["accent_slots"],message["max_line"])
        if len(encoded)!=size:
            raise ValueError(f"{message['id']}: keep the original {size}-byte message size, got {len(encoded)}")
        if len(message["lines"])!=len(decode_lines(source[:-1])):
            raise ValueError("Original line count must be preserved")
        changes.append((offset,encoded))
    font=int(config["font_offset"],16)
    for char,item in config["accent_slots"].items():
        base=font+(ord(item["base"])-config["font_first_code"])*16
        pixels=decode_tile(rom[base:base+16])
        if any(pixels[0]):
            raise ValueError("Glyph top margin changed")
        # Drop one repeated stem row, keeping crossbar, baseline and outline.
        pixels=[[0]*8,[0]*8]+[pixels[y][:] for y in (1,2,3,4,6,7)]
        points=((4,0),(3,1)) if item["mark"]=="acute" else ((3,0),(2,1),(4,1))
        if item["mark"] not in ("acute","circumflex"):
            raise ValueError("Unsupported accent mark")
        for x,y in points: pixels[y][x]=1
        for x,y in points:
            if x+1<8 and pixels[y][x+1]==0: pixels[y][x+1]=2
        destination=font+(item["code"]-config["font_first_code"])*16
        changes.append((destination,encode_tile(pixels)))
    return changes,{"messages":len(config["messages"]),"accented_glyphs":len(config["accent_slots"]),
                    "message_sizes_and_line_counts_preserved":True,"text_pointers_changed":False,
                    "english_only_font_slots":True}
