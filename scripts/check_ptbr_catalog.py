"""Check private editorial drafts for protected names and inventory integrity.

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
    if len(reviewed) != len(draft["records"]) or source.keys() != reviewed.keys():
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original", required=True, type=Path)
    parser.add_argument("--draft", required=True, type=Path)
    parser.add_argument("--rom", required=True, type=Path)
    args = parser.parse_args()
    original = json.loads(args.original.read_text(encoding="utf-8"))
    draft = json.loads(args.draft.read_text(encoding="utf-8"))
    policy = json.loads((ROOT / "localization/pt-BR/policy.json").read_text(encoding="utf-8"))
    profile = json.loads((ROOT / "config/roms/usa-rev1.json").read_text(encoding="utf-8"))
    errors = validate(original, draft, policy)
    digest = hashlib.sha256(args.rom.read_bytes()).hexdigest()
    if digest != original.get("rom_sha256") or digest != profile["sha256"]:
        errors.append("ROM changed or does not match the pinned Rev 1 profile")
    print(json.dumps({"passed": not errors, "errors": errors,
                      "statuses": dict(Counter(r["status"] for r in draft["records"])),
                      "semantic_review_complete": False, "runtime_modified": False}, ensure_ascii=False))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
