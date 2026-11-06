"""Real files and separate processes, using synthetic cartridge RAM only."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXE = ROOT / "build/usa-rev1/rev1_saves_io_tests.exe"
TEMP_ROOT = ROOT / "evidence/save-io-tests"

def pattern(seed):
    return bytes((i * 37 + seed) & 255 for i in range(2048))

@unittest.skipUnless(os.name == "nt", "Windows file locking and Unicode paths")
class SaveStorageTests(unittest.TestCase):
    def setUp(self):
        TEMP_ROOT.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=TEMP_ROOT)
        assert Path(self.temporary.name).resolve().is_relative_to(TEMP_ROOT.resolve())
        self.addCleanup(self.temporary.cleanup)
        self.user = Path(self.temporary.name)
        self.battery = self.user / "saves/save.srm"

    def run_fixture(self, action, seed=7, expected=0):
        result = subprocess.run([str(EXE), str(self.user), action, str(seed)],
                                capture_output=True, timeout=10)
        self.assertEqual(result.returncode, expected, result.stderr.decode(errors="replace"))
        return result.stdout

    def seed(self, data):
        self.battery.parent.mkdir(exist_ok=True)
        self.battery.write_bytes(data)

    def test_first_launch_does_not_write_unchanged_ram(self):
        self.assertEqual(self.run_fixture("read"), bytes(2048))
        self.assertFalse(self.battery.exists())

    def test_roundtrip_and_backup_across_processes(self):
        self.run_fixture("write", 17)
        self.assertEqual(self.battery.read_bytes(), pattern(17))
        self.assertEqual(self.run_fixture("read"), pattern(17))
        self.run_fixture("write", 91)
        self.assertEqual(self.battery.read_bytes(), pattern(91))
        self.assertEqual(self.battery.with_suffix(".srm.bak").read_bytes(), pattern(17))

    def test_malformed_files_are_preserved(self):
        for size in (2047, 2049):
            with self.subTest(size=size):
                data = bytes([0x5a]) * size
                self.seed(data)
                self.run_fixture("read", expected=3)
                self.assertEqual(self.battery.read_bytes(), data)
                self.assertFalse(self.battery.with_suffix(".srm.bak").exists())

    def test_failed_write_preserves_previous_file_and_retry_commits(self):
        self.seed(pattern(11))
        self.run_fixture("block", 73)
        self.assertEqual(self.battery.read_bytes(), pattern(11))
        self.run_fixture("retry", 73)
        self.assertEqual(self.battery.read_bytes(), pattern(73))

    def test_backup_failure_refuses_open_without_replacing_save(self):
        self.seed(pattern(31))
        self.battery.with_suffix(".srm.bak").mkdir()
        self.run_fixture("write", expected=3)
        self.assertEqual(self.battery.read_bytes(), pattern(31))

    def test_only_one_writer_can_open_the_same_profile(self):
        holder = subprocess.Popen([str(EXE), str(self.user), "hold"],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            self.assertEqual(holder.stdout.readline().strip(), b"READY")
            self.run_fixture("write", expected=3)
            self.assertFalse(self.battery.exists())
        finally:
            holder.communicate(b"\n", timeout=10)
        self.assertEqual(holder.returncode, 0)
        self.run_fixture("write")

    def test_unicode_profile_directory(self):
        self.user = self.user / "dados-\u00e1-\u6c49\u5b57"
        self.user.mkdir()
        self.battery = self.user / "saves/save.srm"
        self.run_fixture("write", 29)
        self.assertEqual(self.run_fixture("read"), pattern(29))

if __name__ == "__main__":
    unittest.main()
