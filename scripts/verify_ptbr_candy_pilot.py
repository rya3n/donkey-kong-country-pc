"""Compare Candy's first and second messages, fading and guest-memory effects."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
from verify_ptbr_menu_pilot import ppm_pixels

ROOT=Path(__file__).resolve().parents[1]
# The original text renderer stores its half-cell horizontal adjustment here.
# Every other WRAM byte must match, not just a list of selected game variables.
DIALOGUE_LAYOUT_BYTES={0x068d,0x068e,0x0697,0x0698,0x06a1,0x06a2}
# Three words at $0687 + X, with the renderer's X = 6, 16, 26.
# Greeting and instructions exercise different lines; the remainder is exact.
EXPECTED_LAYOUT_CHANGES={4350:{0x06a1,0x06a2},4500:{0x06a1,0x06a2},
                         4650:{0x068d,0x068e,0x0697,0x0698}}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom",required=True,type=Path)
    parser.add_argument("--out",required=True,type=Path)
    args=parser.parse_args()
    out=args.out.resolve()
    if not out.is_relative_to(ROOT/"evidence"):
        parser.error("Evidence must stay in ignored evidence/")
    out.mkdir(parents=True,exist_ok=False)
    manifest=json.loads((ROOT/"experimental/usa-rev1/pt-BR/menu-pilot/manifest.json").read_text())
    results=[]
    for frames in (4350,4500,4650):
        reports={}
        for kind,build in (("baseline","usa-rev1"),("pilot","ptbr-pilot")):
            folder=out/f"{frames}-{kind}";folder.mkdir()
            env={k:v for k,v in os.environ.items() if not k.startswith("DKC_REV1_") and k!="DKC1_PACING_LOG"}
            env.update(DKC_REV1_TEST_ENTRANCE="FA",DKC_REV1_WRAM_DUMP=str(folder/"wram.bin"),
                       SNESRECOMP_TIER2_DIR=str(folder),SNESRECOMP_TIER2_MANIFEST=str(folder/"tier2.json"))
            run=subprocess.run([str(ROOT/f"build/{build}/dkc_rev1_headless.exe"),str(args.rom.resolve()),
                                str(frames),str(folder/"frame"),str(ROOT/"recipes/usa-rev1/boot-to-jungle.inputs")],
                               env=env,capture_output=True,timeout=120)
            (folder/"stdout.log").write_bytes(run.stdout);(folder/"stderr.log").write_bytes(run.stderr)
            if run.returncode: raise RuntimeError(f"{kind} exited {run.returncode}")
            if kind=="pilot" and manifest["patchset_sha256"].encode() not in run.stderr:
                raise AssertionError("Pilot binary does not match the generated patchset")
            reports[kind]=json.loads(run.stdout)
            ram=(folder/"wram.bin").read_bytes()
            if len(ram)!=131072 or hashlib.sha256(ram).hexdigest()!=reports[kind]["wram_sha256"]:
                raise AssertionError("WRAM evidence does not match its report")
        a,b=reports["baseline"],reports["pilot"]
        for field in ("audio_chain_sha256","dispatch_entries","audio_active_frames"):
            if a[field]!=b[field]: raise AssertionError(f"{field} diverged")
        if b["interpreted_steps"]-a["interpreted_steps"]!=19:
            raise AssertionError("Unexpected execution difference from dialogue centering")
        ram_a=(out/f"{frames}-baseline/wram.bin").read_bytes()
        ram_b=(out/f"{frames}-pilot/wram.bin").read_bytes()
        changed_ram=[i for i,(x,y) in enumerate(zip(ram_a,ram_b)) if x!=y]
        if set(changed_ram)-DIALOGUE_LAYOUT_BYTES:
            raise AssertionError(f"WRAM changed outside dialogue layout: {changed_ram}")
        if set(changed_ram)!=EXPECTED_LAYOUT_CHANGES[frames]:
            raise AssertionError("Unexpected dialogue-layout adjustment")
        image_a=ppm_pixels(out/f"{frames}-baseline/frame.ppm")
        image_b=ppm_pixels(out/f"{frames}-pilot/frame.ppm")
        changed_pixels=[]
        for i in range(256*224):
            if image_a[i*3:i*3+3]!=image_b[i*3:i*3+3]:
                if not 170<=i//256<212: raise AssertionError("Visual change outside dialogue band")
                changed_pixels.append(i)
        if not changed_pixels: raise AssertionError("Dialogue was not translated")
        result={"frames":frames,"audio_match":True,"wram_changed_offsets":[f"0x{i:04X}" for i in changed_ram],
                "outside_dialogue_wram_match":True,"interpreted_steps_delta":19,
                "changed_pixels":len(changed_pixels),"outside_dialogue_pixels_match":True}
        results.append(result)
        print(json.dumps(result),flush=True)
    (out/"results.json").write_text(json.dumps({"patchset_sha256":manifest["patchset_sha256"],
                                               "checkpoints":results},indent=2)+"\n",encoding="utf-8")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
