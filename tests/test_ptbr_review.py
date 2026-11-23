"""Editorial safeguards with synthetic text; no ROM or game dialogue required."""
import copy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("ptbr", Path(__file__).resolve().parents[1] / "scripts/check_ptbr_catalog.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class NameProtectionTests(unittest.TestCase):
    def setUp(self):
        record = dict(id="test", region="dialogue", offset="0x00", end="0x10", byte_length=16,
                      source_lines=["Find Name One!"], source="Find Name One!", policy="translate_in_context",
                      translation=None, status="untranslated")
        self.original = dict(rom_sha256="fixture", records=[record])
        self.draft = copy.deepcopy(self.original)
        self.draft["records"][0].update(translation="Encontre Name One!", status="draft")
        self.policy = dict(protected_terms=["Name One"], context_review_terms=[])

    def test_preserved_name_passes(self):
        self.assertEqual(module.validate(self.original, self.draft, self.policy), [])

    def test_translated_name_fails(self):
        self.draft["records"][0]["translation"] = "Encontre Nome Um!"
        self.assertTrue(any("protected term" in e for e in module.validate(self.original, self.draft, self.policy)))

    def test_mutated_source_fails(self):
        self.draft["records"][0]["offset"] = "0x99"
        self.assertTrue(any("metadata" in e for e in module.validate(self.original, self.draft, self.policy)))

    def test_removed_record_fails(self):
        self.draft["records"].clear()
        self.assertTrue(module.validate(self.original, self.draft, self.policy))

    def test_duplicate_source_record_fails(self):
        self.original["records"].append(copy.deepcopy(self.original["records"][0]))
        self.assertTrue(module.validate(self.original, self.draft, self.policy))

    def test_proper_name_is_not_substring(self):
        self.assertEqual(module.occurrences("Named Ones", "Name One"), 0)

    def test_draft_cannot_self_approve(self):
        self.draft["records"][0]["status"] = "approved"
        self.assertTrue(module.validate(self.original, self.draft, self.policy))


class PilotCoverageTests(unittest.TestCase):
    def test_reports_exact_partial_and_disjoint_ranges(self):
        records = [
            dict(region="dialogue", offset="0x00", end="0x10", translation="Texto próprio"),
            dict(region="dialogue", offset="0x10", end="0x20", translation=None),
            dict(region="credits", offset="0x20", end="0x30", translation=None),
        ]
        regions = [
            dict(offset="0x30", bytes=0x10),
            dict(offset="0x00", bytes=0x10),
            dict(offset="0x12", bytes=0x02),
        ]
        report = module.summarize_manifest_coverage(records, regions, rom_size=0x40)
        self.assertEqual(report, {
            "by_region": {
                "dialogue": dict(records=2, drafted=1, exact_manifest_range=1,
                                 other_overlap=1, no_overlap=0),
                "credits": dict(records=1, drafted=0, exact_manifest_range=0,
                                other_overlap=0, no_overlap=1),
            },
            "manifest_regions": 3,
            "manifest_regions_outside_inventory": 1,
        })

    def test_rejects_manifest_with_invalid_or_overlapping_ranges(self):
        manifests = [
            [],
            [dict(offset="0x00", bytes=0)],
            [dict(offset="0x3F", bytes=2)],
            [dict(offset="0x00", bytes=0x10), dict(offset="0x04", bytes=0x10)],
        ]
        for regions in manifests:
            with self.subTest(regions=regions), self.assertRaises(ValueError):
                module.summarize_manifest_coverage([], regions, rom_size=0x40)


if __name__ == "__main__":
    unittest.main()
