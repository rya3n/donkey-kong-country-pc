"""Read-only check of the pinned source, local ROM and Windows build tools."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]


def git_head(directory: Path) -> str | None:
    if not shutil.which("git") or not directory.is_dir():
        return None
    result = subprocess.run(
        ["git", "-c", f"safe.directory={directory.as_posix()}",
         "-C", str(directory), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def find_toolchain() -> dict:
    locators = [
        Path(os.environ.get("ProgramFiles(x86)", "C:/Program Files (x86)"))
        / "Microsoft Visual Studio/Installer/vswhere.exe",
        Path(os.environ.get("ProgramFiles", "C:/Program Files"))
        / "Microsoft Visual Studio/Installer/vswhere.exe",
    ]
    for locator in locators:
        if not locator.is_file():
            continue
        result = subprocess.run(
            [str(locator), "-latest", "-products", "*", "-requires",
             "Microsoft.VisualStudio.Component.VC.Tools.x86.x64", "-format", "json", "-utf8"],
            capture_output=True, check=False,
        )
        if result.returncode != 0:
            continue
        try:
            instances = json.loads(result.stdout.decode("utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        if not instances or not instances[0].get("isComplete"):
            continue
        instance = instances[0]
        install = Path(instance["installationPath"])
        compilers = sorted(install.glob("VC/Tools/MSVC/*/bin/Hostx64/x64/cl.exe"))
        cmake = install / "Common7/IDE/CommonExtensions/Microsoft/CMake/CMake/bin/cmake.exe"
        ninja = install / "Common7/IDE/CommonExtensions/Microsoft/CMake/Ninja/ninja.exe"
        return {
            "installation": str(install),
            "version": instance.get("installationVersion"),
            "compiler": str(compilers[-1]) if compilers else shutil.which("cl"),
            "cmake": str(cmake) if cmake.is_file() else shutil.which("cmake"),
            "ninja": str(ninja) if ninja.is_file() else shutil.which("ninja"),
            "developer_shell": str(install / "Common7/Tools/VsDevCmd.bat"),
        }
    return {name: shutil.which(name) for name in ("cl", "cmake", "ninja")}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", type=Path, help="Optional local ROM to check")
    parser.add_argument("--json", action="store_true", help="Print machine-readable results")
    args = parser.parse_args()
    lock = json.loads((ROOT / "config/upstream.lock.json").read_text(encoding="utf-8"))
    directories = {
        "upstream": (ROOT / "upstream", lock["commit"]),
        "engine": (ROOT / "upstream/snesrecomp", lock["engine_commit"]),
        "recomp_net": (ROOT / "upstream/snesrecomp/lib/recomp-net", lock["recomp_net_commit"]),
    }
    sources = {}
    for name, (directory, expected) in directories.items():
        actual = git_head(directory)
        sources[name] = {"expected": expected, "actual": actual, "matches": actual == expected}
    candidates = [args.rom.expanduser().resolve()] if args.rom else sorted(
        path for path in ROOT.iterdir() if path.is_file() and path.suffix.lower() in (".smc", ".sfc")
    )
    roms = []
    for path in candidates:
        try:
            size = path.stat().st_size
            with path.open("rb") as stream:
                digest = hashlib.file_digest(stream, "sha256").hexdigest()
        except OSError as error:
            roms.append({"name": path.name, "supported": False, "error": str(error)})
            continue
        roms.append({"name": path.name, "bytes": size, "sha256": digest,
                     "supported": size == lock["rom"]["bytes"] and digest == lock["rom"]["sha256"]})
    toolchain = find_toolchain()
    blockers = []
    if not all(item["matches"] for item in sources.values()):
        blockers.append("Revisoes locais diferentes do lock ou clone ausente.")
    if not any(item["supported"] for item in roms):
        blockers.append("ROM USA v1.0 suportada ainda nao disponivel.")
    if not (toolchain.get("compiler") or toolchain.get("cl")):
        blockers.append("Compilador MSVC x64 nao encontrado.")
    for name in ("cmake", "ninja"):
        if not toolchain.get(name):
            blockers.append(f"Ferramenta {name} nao encontrada.")
    report = {"source_tag": lock["tag"], "sources": sources, "roms": roms,
              "toolchain": toolchain, "blockers": blockers,
              "preflight_passed": not blockers,
              "note": "Deteccao de ferramentas; nao substitui compilacao, testes ou gameplay."}
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=True))
    else:
        print(f"Base: {lock['tag']}")
        for name, source in sources.items():
            print(f"  {name}: {'OK' if source['matches'] else 'PENDENTE'}")
        print(f"  ROM suportada: {'OK' if any(r['supported'] for r in roms) else 'PENDENTE'}")
        print(f"  MSVC: {toolchain.get('compiler') or toolchain.get('cl') or 'PENDENTE'}")
        print(f"  CMake: {toolchain.get('cmake') or 'PENDENTE'}")
        print(f"  Ninja: {toolchain.get('ninja') or 'PENDENTE'}")
        for blocker in blockers:
            print(f"  - {blocker}")
    return 1 if blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())
