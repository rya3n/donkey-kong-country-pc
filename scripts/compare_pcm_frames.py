"""Compare indexed stereo PCM captures and report differences without exporting audio."""
from __future__ import annotations

import argparse
import csv
from hashlib import sha256
import json
from pathlib import Path
import struct


def read_index(path: Path) -> list[tuple[int, int]]:
    with path.open(encoding="utf-8", newline="") as stream:
        rows = csv.DictReader(stream)
        if not {"frame", "samples"}.issubset(rows.fieldnames or ()):
            raise ValueError(f"{path}: expected frame and samples columns")
        index = [(int(row["frame"]), int(row["samples"])) for row in rows]
    if not index or index[0][0] < 1:
        raise ValueError(f"{path}: expected a nonempty, one-based frame index")
    for expected, (frame, samples) in enumerate(index, start=index[0][0]):
        if frame != expected or samples < 1:
            raise ValueError(f"{path}: invalid index entry at frame {expected}")
    return index


def compare(base: Path, pilot: Path) -> dict:
    index = read_index(base / "audio.csv")
    if index != read_index(pilot / "audio.csv"):
        raise ValueError("Captures have different frame indexes or sample counts")
    base_hash = pilot_hash = bytes(32)
    intervals = []
    silence_differences = []
    with (base / "audio.pcm").open("rb") as left, (pilot / "audio.pcm").open("rb") as right:
        for frame, samples in index:
            size = samples * 4
            a, b = left.read(size), right.read(size)
            if len(a) != size or len(b) != size:
                raise ValueError(f"Truncated stereo PCM at frame {frame}")
            base_hash = sha256(base_hash + a).digest()
            pilot_hash = sha256(pilot_hash + b).digest()
            if a == b:
                continue
            unpack = struct.Struct(f"<{samples * 2}h").unpack
            peak_delta = max(abs(x - y) for x, y in zip(unpack(a), unpack(b), strict=True))
            if any(a) != any(b):
                silence_differences.append(frame)
            if intervals and intervals[-1]["last_frame"] == frame - 1:
                interval = intervals[-1]
                interval["last_frame"] = frame
                interval["peak_delta"] = max(interval["peak_delta"], peak_delta)
            else:
                intervals.append({"first_frame": frame, "last_frame": frame, "peak_delta": peak_delta})
        if left.read(1) or right.read(1):
            raise ValueError("Stereo PCM contains data after the last indexed frame")
    return {
        "first_frame": index[0][0],
        "last_frame": index[-1][0],
        "compared_frames": len(index),
        "different_frames": sum(row["last_frame"] - row["first_frame"] + 1 for row in intervals),
        "intervals": intervals,
        "silence_differences": silence_differences,
        "base_audio_chain_sha256": base_hash.hex(),
        "pilot_audio_chain_sha256": pilot_hash.hex(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, required=True, help="Folder containing audio.csv and audio.pcm")
    parser.add_argument("--pilot", type=Path, required=True, help="Folder containing the second capture")
    args = parser.parse_args()
    try:
        report = compare(args.base, args.pilot)
    except (OSError, TypeError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
