"""Check private editorial drafts and optionally compare the inventory with a pilot manifest.

This check does not approve meaning, line layout, font support or runtime use.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def occurrences(text: str, term: str) -> int:
    return len(re.findall(r"(?<!\w)" + re.escape(term) + r"(?!\w)", text, re.IGNORECASE))


def validate(original: dict, draft: dict, policy: dict) -> list[str]:
    errors = []
    source = {r["id"]: r for r in original["records"]}
    reviewed = {r["id"]: r for r in draft["records"]}
    if (len(source) != len(original["records"])
            or len(reviewed) != len(draft["records"])
            or source.keys() != reviewed.keys()):
        errors.append("Catalog IDs were added, removed or duplicated")
    if original.get("rom_sha256") != draft.get("rom_sha256"):
        errors.append("ROM identity changed")
    immutable = ("region", "offset", "end", "byte_length", "source_lines", "source", "policy")
    names = policy["protected_terms"] + policy["context_review_terms"]
    names += [r["source"] for r in source.values()
              if r["policy"] == "preserve_names" and r["source"] != "ERROR"]
    for ident in source.keys() & reviewed.keys():
        old, new = source[ident], reviewed[ident]
        if any(old[field] != new.get(field) for field in immutable):
            errors.append(f"{ident}: source metadata changed")
        translation = new.get("translation")
        if translation is None:
            continue
        if not isinstance(translation, str) or not translation.strip() or "\ufffd" in translation:
            errors.append(f"{ident}: invalid translation")
            continue
        if new.get("status") != "draft":
            errors.append(f"{ident}: this workflow only accepts unapproved drafts")
        if old["policy"] == "preserve_names" and translation != old["source"]:
            errors.append(f"{ident}: protected map label changed")
        for term in set(names):
            expected = occurrences(old["source"], term)
            if expected and occurrences(translation, term) < expected:
                errors.append(f"{ident}: protected term changed or missing: {term}")
    return errors


def summarize_manifest_coverage(
    records: list[dict], regions: list[dict], rom_size: int
) -> dict:
    ranges = []
    for region in regions:
        start = int(region["offset"], 16)
        size = region["bytes"]
        if type(size) is not int or size <= 0 or start < 0 or start + size > rom_size:
            raise ValueError("Pilot manifest contains an invalid byte range")
        ranges.append((start, start + size))
    if not ranges:
        raise ValueError("Pilot manifest has no byte ranges")
    ranges.sort()
    if any(end > next_start for (_, end), (next_start, _) in zip(ranges, ranges[1:])):
        raise ValueError("Pilot manifest byte ranges overlap")

    by_region: dict[str, Counter[str]] = {}
    intersecting = set()
    for record in records:
        start = int(record["offset"], 16)
        end = int(record["end"], 16)
        if not 0 <= start < end <= rom_size:
            raise ValueError("Catalog contains an invalid byte range")
        summary = by_region.setdefault(record["region"], Counter(
            records=0, drafted=0, exact_manifest_range=0, other_overlap=0, no_overlap=0,
        ))
        summary["records"] += 1
        summary["drafted"] += record.get("translation") is not None
        matches = {span for span in ranges if span[0] < end and start < span[1]}
        intersecting.update(matches)
        if (start, end) in matches:
            summary["exact_manifest_range"] += 1
        elif matches:
            summary["other_overlap"] += 1
        else:
            summary["no_overlap"] += 1

    return {
        "by_region": by_region,
        "manifest_regions": len(ranges),
        "manifest_regions_outside_inventory": len(ranges) - len(intersecting),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original", required=True, type=Path)
    parser.add_argument("--draft", required=True, type=Path)
    parser.add_argument("--rom", required=True, type=Path)
    parser.add_argument("--pilot-manifest", type=Path)
    args = parser.parse_args()
    original = json.loads(args.original.read_text(encoding="utf-8"))
    draft = json.loads(args.draft.read_text(encoding="utf-8"))
    policy = json.loads((ROOT / "localization/pt-BR/policy.json").read_text(encoding="utf-8"))
    profile = json.loads((ROOT / "config/roms/usa-rev1.json").read_text(encoding="utf-8"))
    errors = validate(original, draft, policy)
    rom = args.rom.read_bytes()
    digest = hashlib.sha256(rom).hexdigest()
    if digest != original.get("rom_sha256") or digest != profile["sha256"]:
        errors.append("ROM changed or does not match the pinned Rev 1 profile")
    report = {"passed": not errors, "errors": errors,
              "statuses": dict(Counter(r["status"] for r in draft["records"])),
              "semantic_review_complete": False, "runtime_modified": False}
    if args.pilot_manifest and not errors:
        try:
            manifest = json.loads(args.pilot_manifest.read_text(encoding="utf-8"))
            if manifest.get("rom_sha256") != digest:
                raise ValueError("Pilot manifest does not match the pinned Rev 1 ROM")
            report["pilot_coverage"] = summarize_manifest_coverage(
                draft["records"], manifest["regions"], len(rom)
            )
        except (AttributeError, KeyError, OSError, TypeError, ValueError) as error:
            errors.append(f"Could not compare pilot coverage: {error}")
            report["passed"] = False
    print(json.dumps(report, ensure_ascii=False))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
