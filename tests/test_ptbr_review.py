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

    def test_proper_name_is_not_substring(self):
        self.assertEqual(module.occurrences("Named Ones", "Name One"), 0)

    def test_draft_cannot_self_approve(self):
        self.draft["records"][0]["status"] = "approved"
        self.assertTrue(module.validate(self.original, self.draft, self.policy))


if __name__ == "__main__":
    unittest.main()
