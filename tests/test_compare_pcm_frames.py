"""Synthetic frame alignment and signed PCM checks."""
from pathlib import Path
import importlib.util
import struct
import tempfile
import unittest


spec = importlib.util.spec_from_file_location(
    "compare_pcm_frames", Path(__file__).resolve().parents[1] / "scripts/compare_pcm_frames.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PcmFrameTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name) / "base"
        self.pilot = Path(temp.name) / "pilot"
        for folder in (self.base, self.pilot):
            folder.mkdir()
            (folder / "audio.csv").write_text("frame,samples\n10,1\n11,1\n12,1\n13,1\n14,1\n")

    def write_pcm(self, base, pilot):
        for folder, samples in ((self.base, base), (self.pilot, pilot)):
            (folder / "audio.pcm").write_bytes(struct.pack(f"<{len(samples)}h", *samples))

    def test_groups_differences_and_measures_signed_sample_delta(self):
        self.write_pcm(
            (7, 8, 0, 0, -32768, 0, 11, 12, 17, 18),
            (7, 8, 2, 1, 32767, 0, 11, 12, 17, 19),
        )
        report = module.compare(self.base, self.pilot)
        self.assertEqual(report["different_frames"], 3)
        self.assertEqual(report["intervals"], [
            {"first_frame": 11, "last_frame": 12, "peak_delta": 65535},
            {"first_frame": 14, "last_frame": 14, "peak_delta": 1},
        ])
        self.assertEqual(report["silence_differences"], [11])

    def test_rejects_indexes_with_different_sample_counts(self):
        index = self.pilot / "audio.csv"
        index.write_text(index.read_text().replace("11,1", "11,2"))
        with self.assertRaisesRegex(ValueError, "different frame indexes or sample counts"):
            module.compare(self.base, self.pilot)

    def test_rejects_pcm_that_does_not_fit_the_index(self):
        for length in (8, 12):
            with self.subTest(length=length):
                self.write_pcm((0,) * 10, (0,) * length)
                with self.assertRaises(ValueError):
                    module.compare(self.base, self.pilot)


if __name__ == "__main__":
    unittest.main()
