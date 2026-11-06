"""Compare separate baseline/pilot builds at menu checkpoints and gameplay.

Headless runs use no personal saves. Screenshots and reports stay private.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import subprocess
from generate_ptbr_menu_pilot import make_patch
from generate_ptbr_candy_pilot import make_candy_patch
from generate_ptbr_funky_pilot import make_funky_patch
from generate_ptbr_cranky_pilot import make_cranky_patch

ROOT = Path(__file__).resolve().parents[1]


def ppm_pixels(path: Path) -> bytes:
    data = path.read_bytes()
    header = b"P6\n256 224\n255\n"
    if not data.startswith(header) or len(data) != len(header)+256*224*3:
        raise ValueError("Unexpected snapshot format")
    return data[len(header):]


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom",required=True,type=Path)
    parser.add_argument("--out",required=True,type=Path)
    args=parser.parse_args()
    out=args.out.resolve()
    if not out.is_relative_to(ROOT/"evidence"):
        parser.error("Evidence must remain in ignored evidence/")
    out.mkdir(parents=True,exist_ok=False)
    original_rom=args.rom.read_bytes()
    config=json.loads((ROOT/"localization/pt-BR/menu-pilot.json").read_text(encoding="utf-8"))
    patches,_=make_patch(original_rom,config)
    candy_config=json.loads((ROOT/"localization/pt-BR/candy-pilot.json").read_text(encoding="utf-8"))
    candy_patches,_=make_candy_patch(original_rom,candy_config)
    patches+=candy_patches
    funky_config=json.loads((ROOT/"localization/pt-BR/funky-pilot.json").read_text(encoding="utf-8"))
    funky_patches,_=make_funky_patch(original_rom,funky_config,candy_config)
    patches+=funky_patches
    cranky_config=json.loads((ROOT/"localization/pt-BR/cranky-pilot.json").read_text(encoding="utf-8"))
    cranky_patches,_=make_cranky_patch(original_rom,cranky_config,candy_config)
    patches+=cranky_patches
    translated_bytes={i for msg in candy_config["messages"]+funky_config["messages"]+cranky_config["messages"]
                      for i in range(int(msg["offset"],16),int(msg["offset"],16)+msg["bytes"])}
    patched_rom=bytearray(original_rom)
    for offset,data in patches: patched_rom[offset:offset+len(data)]=data
    regions=json.loads((ROOT/"localization/pt-BR/regions.json").read_text(encoding="utf-8"))["regions"]
    for region in regions:
        start,end=int(region["start"],16),int(region["end"],16)
        if any(original_rom[i]!=patched_rom[i] for i in range(start,end) if i not in translated_bytes):
            raise AssertionError("Untranslated text region changed")
    # Every original tile referenced by the Kongs' side must retain its bytes.
    import struct
    mode=config["player_select"]
    tm,gfx=int(mode["tilemap"],16),int(mode["graphics"],16)
    for i in range(int(mode["tilemap_size"],16)//2):
        if i%32>=mode["clear_text_from_x"]: continue
        if original_rom[tm+i*2:tm+i*2+2]!=patched_rom[tm+i*2:tm+i*2+2]:
            raise AssertionError("Kong tilemap changed")
        tile=struct.unpack_from('<H',original_rom,tm+i*2)[0]&1023
        start=gfx+tile*32
        if original_rom[start:start+32]!=patched_rom[start:start+32]:
            raise AssertionError("Kong graphics changed")
    print("Protected names, untranslated text and Kong graphics match the original",flush=True)
    manifest=json.loads((ROOT/"experimental/usa-rev1/pt-BR/menu-pilot/manifest.json").read_text())
    reports=[]
    for frames,rois in ((1700,[(32,23,224,42),(32,183,120,202)]),
                        (2300,[(80,0,256,224)]),(4800,[])):
        runs={}
        for kind,build in (("baseline","usa-rev1"),("pilot","ptbr-pilot")):
            run_dir=out/f"{frames}-{kind}"
            run_dir.mkdir()
            env={k:v for k,v in os.environ.items() if not k.startswith("DKC_REV1_") and k!="DKC1_PACING_LOG"}
            env.update(SNESRECOMP_TIER2_DIR=str(run_dir),SNESRECOMP_TIER2_MANIFEST=str(run_dir/"tier2.json"))
            run=subprocess.run([str(ROOT/f"build/{build}/dkc_rev1_headless.exe"),str(args.rom.resolve()),
                                str(frames),str(run_dir/"frame"),str(ROOT/"recipes/usa-rev1/boot-to-jungle.inputs")],
                               env=env,capture_output=True,timeout=120)
            (run_dir/"stdout.log").write_bytes(run.stdout)
            (run_dir/"stderr.log").write_bytes(run.stderr)
            if run.returncode: raise RuntimeError(f"{kind} exited {run.returncode}")
            if kind=="pilot" and manifest["patchset_sha256"].encode() not in run.stderr:
                raise AssertionError("Pilot binary contains stale generated data")
            runs[kind]=json.loads(run.stdout)
        keys=("wram_sha256","audio_chain_sha256","interpreted_steps","dispatch_entries","audio_active_frames")
        for key in keys:
            if runs["baseline"][key]!=runs["pilot"][key]:
                raise AssertionError(f"{frames}: {key} diverged")
        before=ppm_pixels(out/f"{frames}-baseline/frame.ppm")
        after=ppm_pixels(out/f"{frames}-pilot/frame.ppm")
        differences=0
        for pixel in range(256*224):
            if before[pixel*3:pixel*3+3]!=after[pixel*3:pixel*3+3]:
                differences+=1
                x,y=pixel%256,pixel//256
                if not any(x0<=x<x1 and y0<=y<y1 for x0,y0,x1,y1 in rois):
                    raise AssertionError(f"{frames}: unexpected visual change at {x},{y}")
        if rois and not differences: raise AssertionError("Menu did not change")
        reports.append({"frames":frames,"guest_state_and_audio_match":True,"changed_pixels":differences,
                        "outside_text_regions_match":True,"frame_sha256":runs["pilot"]["frame_sha256"]})
        print(f"frames={frames}: state/audio match, changed_pixels={differences}, outside text regions match",flush=True)
    (out/"results.json").write_text(json.dumps({"protected_names_untranslated_text_and_kong_graphics_match":True,
                                               "checkpoints":reports},indent=2)+"\n",encoding="utf-8")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
