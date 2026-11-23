"""Compare the Candy dialogue, save menu and return to the map in both builds."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess

from verify_ptbr_menu_pilot import ppm_pixels

ROOT = Path(__file__).resolve().parents[1]
ENTRANCE = 0xFA
BUILDS = {"base": "usa-rev1", "pilot": "ptbr-pilot"}
CHECKPOINTS = {"dialogue": 4440, "save_menu": 4800, "map": 4936}
MATCHED_FIELDS = ("sram_sha256", "entrance")
TITLE_ROWS = range(24, 56)


def run_checkpoint(rom: Path, recipe: Path, build: str, frames: int, folder: Path) -> dict:
    folder.mkdir()
    env = {key: value for key, value in os.environ.items()
           if not key.startswith(("DKC_REV1_", "DKC1_", "SNESRECOMP_"))}
    env.update(
        DKC_REV1_SAVE_DIR=str(folder),
        DKC_REV1_TEST_ENTRANCE=f"{ENTRANCE:x}",
        SNESRECOMP_TIER2_DIR=str(folder),
        SNESRECOMP_TIER2_MANIFEST=str(folder / "tier2.json"),
    )
    exe = ROOT / "build" / build / "dkc_rev1_headless.exe"
    run = subprocess.run(
        [str(exe), str(rom), str(frames), str(folder / "frame"), str(recipe)],
        capture_output=True, env=env, timeout=120,
    )
    (folder / "stdout.log").write_bytes(run.stdout)
    (folder / "stderr.log").write_bytes(run.stderr)
    if run.returncode:
        raise RuntimeError(f"{build} exited {run.returncode} at frame {frames}. See {folder}")
    report = json.loads(run.stdout)
    if report["frames"] != frames or report["entrance"] != ENTRANCE or report["sram_size"] != 2048:
        raise AssertionError(f"{build}: unexpected Candy checkpoint at frame {frames}")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    rom = args.rom.resolve(strict=True)
    out = args.out.resolve()
    if not out.is_relative_to(ROOT / "evidence"):
        parser.error("Evidence must remain in ignored evidence/")
    out.mkdir(parents=True, exist_ok=False)

    source = (ROOT / "recipes/usa-rev1/candy-save.inputs").read_text(encoding="ascii")
    recipe = out / "visit.inputs"
    recipe.write_text(source.rstrip() + "\n0001 1\n0000 135\n", encoding="ascii")
    manifest_path = ROOT / "experimental/usa-rev1/pt-BR/menu-pilot/manifest.json"
    patchset = json.loads(manifest_path.read_text(encoding="utf-8"))["patchset_sha256"]
    comparisons = {}
    for checkpoint, frames in CHECKPOINTS.items():
        folders = {kind: out / f"{checkpoint}-{kind}" for kind in BUILDS}
        with ThreadPoolExecutor(max_workers=len(BUILDS)) as pool:
            runs = {kind: pool.submit(run_checkpoint, rom, recipe, build, frames, folders[kind])
                    for kind, build in BUILDS.items()}
            results = {kind: run.result() for kind, run in runs.items()}
        if patchset.encode("ascii") not in (folders["pilot"] / "stderr.log").read_bytes():
            raise AssertionError("Pilot executable does not match the local manifest")
        for field in MATCHED_FIELDS:
            if results["base"][field] != results["pilot"][field]:
                raise AssertionError(f"{checkpoint}: {field} differs between builds")
        base = ppm_pixels(folders["base"] / "frame.ppm")
        pilot = ppm_pixels(folders["pilot"] / "frame.ppm")
        changed_pixels = [pixel for pixel in range(256 * 224)
                          if base[pixel * 3:pixel * 3 + 3] != pilot[pixel * 3:pixel * 3 + 3]]
        comparison = {
            "frames": frames,
            "changed_pixels": len(changed_pixels),
            "entrance_and_sram_match": True,
            "wram_matches": results["base"]["wram_sha256"] == results["pilot"]["wram_sha256"],
            "audio_chain_matches": (
                results["base"]["audio_chain_sha256"] == results["pilot"]["audio_chain_sha256"]
            ),
        }
        if checkpoint == "dialogue" and (
            not changed_pixels or any(not 170 <= pixel // 256 < 212 for pixel in changed_pixels)
        ):
            raise AssertionError("Expected the localized dialogue to change inside its text band")
        if checkpoint == "save_menu":
            comparison["changed_pixels_in_title_band"] = sum(
                pixel // 256 in TITLE_ROWS for pixel in changed_pixels
            )
        if checkpoint == "map":
            if changed_pixels:
                raise AssertionError("The map changed between builds")
            save = (folders["pilot"] / "saves/save.srm").read_bytes()
            if (len(save) != 2048 or save != (folders["base"] / "saves/save.srm").read_bytes()
                    or sha256(save).hexdigest() != results["pilot"]["sram_sha256"]):
                raise AssertionError("The saved SRAM differs between builds or from the runtime report")
        comparisons[checkpoint] = comparison
        print(json.dumps({checkpoint: comparison}), flush=True)

    (out / "results.json").write_text(
        json.dumps({"checkpoints": comparisons, "saved_sram_matches": True}, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
