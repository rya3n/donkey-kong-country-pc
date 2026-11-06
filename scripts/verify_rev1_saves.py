"""Three Candy saves and cold restarts, isolated from personal progress."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    rom = args.rom.resolve(strict=True)
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    reports = []
    desktop = ROOT / "build/usa-rev1/DKC-Rev1-Teste.exe"
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = subprocess.SW_HIDE
    for repeat in range(1, 4):
        repeat_dir = out / str(repeat)
        repeat_dir.mkdir()
        users = {kind: repeat_dir / (kind + "-user") for kind in ("headless", "desktop")}
        for directory in users.values():
            directory.mkdir()
        saved_images = {}
        for leg in ("save", "cold"):
            recipe = ROOT / "recipes/usa-rev1" / ("candy-save.inputs" if leg == "save" else "cold-load.inputs")
            leg_dir = repeat_dir / leg
            leg_dir.mkdir()
            results = {}
            for kind in ("headless", "desktop"):
                evidence = leg_dir / kind
                evidence.mkdir()
                env = os.environ.copy()
                for key in list(env):
                    if key.startswith("DKC_REV1_") or key == "DKC1_PACING_LOG":
                        env.pop(key)
                env.update(DKC_REV1_SAVE_DIR=str(users[kind]),
                           SNESRECOMP_TIER2_DIR=str(evidence),
                           SNESRECOMP_TIER2_MANIFEST=str(evidence / "tier2.json"))
                if leg == "save":
                    env["DKC_REV1_TEST_ENTRANCE"] = "FA"
                if kind == "headless":
                    run = subprocess.run([str(ROOT / "build/usa-rev1/dkc_rev1_headless.exe"), str(rom),
                                          "4801", str(evidence / "frame"), str(recipe)],
                                         env=env, capture_output=True, timeout=90)
                    (evidence / "stdout.log").write_bytes(run.stdout)
                    (evidence / "stderr.log").write_bytes(run.stderr)
                    if run.returncode:
                        raise RuntimeError(f"Headless failed: {evidence}, exit {run.returncode}")
                    report = json.loads(run.stdout)
                else:
                    env.update(DKC_REV1_BENCH_FRAMES="1", DKC_REV1_PREPARE_INPUT=str(recipe),
                               DKC_REV1_TEST_ROM=str(rom))
                    run = subprocess.run([str(desktop), "--jungle"], env=env, startupinfo=startup, timeout=90)
                    log = (desktop.parent / "DKC-Rev1-teste.log").read_text(errors="replace")
                    (evidence / "desktop.log").write_text(log, encoding="utf-8")
                    if run.returncode:
                        raise RuntimeError(f"Desktop failed: {evidence}, exit {run.returncode}")
                    report = {key: re.search(r"benchmark_" + label + r"=(\w+)", log)[1]
                              for key, label in (("frame_sha256", "frame_sha256"),
                                                 ("wram_sha256", "wram_sha256"),
                                                 ("sram_sha256", "sram_sha256"))}
                    report["entrance"] = int(re.search(r"benchmark_entrance=(\d+)", log)[1])
                    if "saves_enabled=1" not in log:
                        raise AssertionError("Desktop persistence was not enabled")
                    if leg == "cold" and "[sram] loaded" not in log:
                        raise AssertionError("Cold desktop did not load SRAM from disk")
                battery = users[kind] / "saves/save.srm"
                data = battery.read_bytes()
                assert len(data) == 2048
                assert hashlib.sha256(data).hexdigest() == report["sram_sha256"]
                if leg == "save":
                    saved_images[kind] = data
                else:
                    assert data == saved_images[kind], "Cold boot changed the Candy fixture"
                    assert battery.with_suffix(".srm.bak").read_bytes() == saved_images[kind]
                assert report["entrance"] == 0xfa, report
                results[kind] = report
            for key in ("frame_sha256", "wram_sha256", "sram_sha256", "entrance"):
                assert results["desktop"][key] == results["headless"][key], (leg, key, results)
            reports.append({"repeat": repeat, "leg": leg, "matched": True,
                            "frame_sha256": results["headless"]["frame_sha256"],
                            "sram_sha256": results["headless"]["sram_sha256"]})
            print(f"repeat={repeat} leg={leg}: desktop/headless/disk match", flush=True)
    assert len({report["sram_sha256"] for report in reports}) == 1
    (out / "results.json").write_text(json.dumps(reports, indent=2), encoding="utf-8")
    print("Candy save and cold restart passed three times; no snapshots used.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
