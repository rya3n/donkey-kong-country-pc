"""Generate private USA Rev 1 C from a hash-pinned local ROM and new cfg roots."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from check_project import ROOT, git_head


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", required=True, type=Path)
    parser.add_argument("--profile-manifest", action="append", default=[], type=Path)
    args = parser.parse_args()
    profile = json.loads((ROOT / "config/roms/usa-rev1.json").read_text(encoding="utf-8"))
    lock = json.loads((ROOT / "config/upstream.lock.json").read_text(encoding="utf-8"))
    for directory, expected in ((ROOT / "upstream", lock["commit"]),
                                (ROOT / "upstream/snesrecomp", lock["engine_commit"])):
        if git_head(directory) != expected:
            raise ValueError(f"Pinned source revision mismatch: {directory.name}")
    rom = args.rom.expanduser().resolve(strict=True)
    with rom.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    if rom.stat().st_size != profile["bytes"] or digest != profile["sha256"]:
        raise ValueError("Expected the exact USA Rev 1 ROM from config/roms/usa-rev1.json")
    config = ROOT / profile["config_directory"]
    output = ROOT / profile["generated_directory"]
    tools = ROOT / "upstream/snesrecomp/tools"
    subprocess.run([sys.executable, str(tools / "v2_sync_funcs_h.py"),
                    "--cfg-dir", str(config), "--out", str(config / "funcs.h")], check=True)
    command = [sys.executable, str(tools / "v2_emit.py"), "--rom", str(rom),
               "--cfg-dir", str(config), "--out-dir", str(output),
               "--no-host-root-scan", "--no-hle", "--cfg-roots",
               "--analysis-backend", "python", "--max-insns", "4096",
               "--max-nodes", "100000"]
    for manifest in args.profile_manifest:
        recorded = json.loads(manifest.read_text(encoding="utf-8"))
        if recorded.get("rom_title") != "dkc1-usa-rev1-experimental":
            raise ValueError("Coverage profile is not from the USA Rev 1 experimental host")
        command.extend(["--profile-manifest", str(manifest.resolve(strict=True))])
    subprocess.run(command, check=True)
    (output / "source_identity.json").write_text(json.dumps({
        "rom_sha256": digest, "rom_profile": profile["id"],
        "upstream_commit": lock["commit"], "engine_commit": lock["engine_commit"],
        "experimental": True, "game_compatibility_validated": False,
    }, indent=2), encoding="utf-8")
    print("Private experimental sources generated; gameplay remains unvalidated.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
