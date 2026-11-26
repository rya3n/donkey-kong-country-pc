"""Localize the ship's scrolling credits within their original ROM bounds."""
from __future__ import annotations

import re

from generate_ptbr_candy_pilot import encode_message
from inventory_rev1_text import decode_lines

START = 0x01EFFC
STOP = 0x01F08E
MAX_COLUMNS = 24


def make_ship_credits_patch(
    rom: bytes, config: dict, accents: dict
) -> tuple[int, bytes]:
    if (rom[0x01EECF:0x01EED2] != bytes.fromhex("a9 fc ef")
            or rom[0x01EEDD:0x01EEE0] != bytes.fromhex("a9 8e f0")):
        raise ValueError("Rev 1 ship credits pointer guard failed")
    source = rom[START:STOP].split(b"\0")
    if (len(source) != 9 or source[-1] != b"" or rom[STOP] != 0
            or source[6] != b"\xa0" or source[0][:2] != b"\xa0\xa0"
            or len(decode_lines(source[0])) != 3 or len(decode_lines(source[7])) != 1):
        raise ValueError("Rev 1 ship credits layout guard failed")

    title = source[0][:2] + encode_message([config["title"]], accents, MAX_COLUMNS)
    roles = config["roles"]
    if len(roles) != 5:
        raise ValueError("Expected five roles in the ship credits")
    credits = [title]
    for original, role in zip(source[1:6], roles):
        line, = decode_lines(original)
        columns = re.fullmatch(r"[A-Z]+(?: [A-Z]+)*(\.{2,})([^.].*)", line)
        if columns is None:
            raise ValueError("Ship credit attribution does not have a dotted leader")
        name = columns[2]
        leader = columns.start(2) - len(role)
        if leader < 2:
            raise ValueError(f"Ship credit role does not fit its column: {role}")
        credits.append(encode_message([role + "." * leader + name], accents, MAX_COLUMNS))

    # The end pointer stays fixed. Use the slack on the question line for
    # the longer title while preserving the same line and group transitions.
    width = len(source[7]) + len(source[0]) + 1 - len(title)
    question = config["question"]
    if len(question) > width or not question.endswith("?"):
        raise ValueError("Ship credits question does not fit its line")
    credits.extend((source[6] + b"\0", encode_message([question.center(width)], accents, MAX_COLUMNS)))
    data = b"".join(credits)
    if len(data) != STOP - START:
        raise ValueError("Ship credits exceed their original ROM block")
    return START, data
