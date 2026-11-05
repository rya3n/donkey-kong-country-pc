"""Sample fresh diagnostic entrances; this is not a campaign playthrough."""
from __future__ import annotations
import argparse
import csv
import json
import os
from pathlib import Path
import statistics
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
# Structural entry identifiers consulted in Yoshifanatic1's DKC1 disassembly.
# Names/IDs are research leads; actual Rev 1 screenshots qualify scene identity.
LEVELS = [
    ("Jungle Hijinxs", "16"), ("Ropey Rampage", "0C"),
    ("Reptile Rumble", "EA"), ("Coral Capers", "BF"),
    ("Barrel Cannon Canyon", "17"), ("Very Gnawtys Lair", "E0"),
    ("Winkys Walkway", "D9"), ("Mine Cart Carnage", "2E"),
    ("Bouncy Bonanza", "07"), ("Stop And Go Station", "31"),
    ("Millstone Mayhem", "42"), ("Neckys Nuts", "E1"),
    ("Vulture Culture", "A5"), ("Tree Top Town", "A4"),
    ("Forest Frenzy", "D0"), ("Temple Tempest", "43"),
    ("Orangutan Gang", "0D"), ("Clam City", "DE"), ("Bumble B Rumble", "E5"),
    ("Snow Barrel Blast", "24"), ("Slipslide Ride", "6D"),
    ("Ice Age Alley", "A7"), ("Croctopus Chase", "3E"),
    ("Torchlight Trouble", "14"), ("Rope Bridge Rumble", "CE"),
    ("Really Gnawty Rampage", "E2"), ("Oil Drum Alley", "40"),
    ("Trick Track Trek", "2F"), ("Elevator Antics", "18"),
    ("Poison Pond", "22"), ("Mine Cart Madness", "27"),
    ("Blackout Basement", "41"), ("Boss Dumb Drum", "E3"),
    ("Tanked Up Trouble", "30"), ("Manic Mincers", "12"),
    ("Misty Mine", "0A"), ("Loopy Lights", "36"),
    ("Platform Perils", "2B"), ("Neckys Revenge", "E4"),
    ("Gang Plank Galleon", "68"),
]

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--only", action="append", default=[], help="Entry ID in hexadecimal; repeat to select cases")
    parser.add_argument("--frames", type=int, default=5100)
    args = parser.parse_args()
    if not 4351 <= args.frames <= 20000:
        parser.error("--frames must be 4351..20000")
    selected = {value.lower() for value in args.only}
    if selected - {entrance.lower() for _, entrance in LEVELS}:
        parser.error("--only must name a known hexadecimal entrance ID")
    rom = args.rom.resolve(strict=True)
    output = args.out.resolve()
    output.mkdir(parents=True, exist_ok=False)
    results = []
    for name, entrance in LEVELS:
        if selected and entrance.lower() not in selected:
            continue
        directory = output / (entrance + "-" + name.lower().replace(" ", "-"))
        directory.mkdir()
        env = os.environ.copy()
        env.update(DKC_REV1_TEST_ENTRANCE=entrance,
                   DKC_REV1_TIMING_FILE=str(directory / "timing.csv"),
                   SNESRECOMP_TIER2_DIR=str(directory),
                   SNESRECOMP_TIER2_MANIFEST=str(directory / "tier2.json"))
        with (directory / "stdout.log").open("w") as stdout, (directory / "stderr.log").open("w") as stderr:
            run = subprocess.run([str(ROOT / "build/usa-rev1/dkc_rev1_headless.exe"),
                                  str(rom), str(args.frames), str(directory / "frame"),
                                  str(ROOT / "recipes/usa-rev1/boot-to-jungle.inputs")],
                                 env=env, stdout=stdout, stderr=stderr, timeout=90)
        result = {"scene": name, "diagnostic_entrance": entrance, "exit": run.returncode,
                  "scope": f"fresh forced entrance, frames 4350..{min(4650,args.frames)-1}; neutral input",
                  "scene_identity": "requires screenshot review", "campaign_validated": False}
        if run.returncode == 0:
            with (directory / "timing.csv").open() as stream:
                rows = list(csv.DictReader(stream))[4350:min(4650,args.frames)]
            values = sorted(float(row["work_ms"]) for row in rows)
            result.update(mean_ms=statistics.fmean(values), p95_ms=values[int(len(values)*.95)],
                          max_ms=max(values), frames_over_budget=sum(v>1000/60.0988 for v in values),
                          samples=len(values), observed_entrances=sorted({r["entrance"] for r in rows}),
                          fingerprint=json.loads((directory / "stdout.log").read_text()))
        results.append(result)
        (output / "summary.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
        print(f"{name}: exit={run.returncode}, p95_ms={result.get('p95_ms')}", flush=True)
    return int(any(row["exit"] for row in results))

if __name__ == "__main__":
    sys.exit(main())
