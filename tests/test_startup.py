import tempfile
import unittest
from pathlib import Path

from src.emulator.shell import Shell
from src.emulator.startup import run_script
from src.emulator.vfs import VirtualFileSystem


class StartupTests(unittest.TestCase):
    def test_stops_at_first_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "start.txt"
            path.write_text("ls\ninvalid\ncd /later\n", encoding="utf-8")
            output = []
            vfs = VirtualFileSystem.from_xml("vfs/minimal.xml")
            success = run_script(str(path), Shell(vfs), output.append)
            self.assertFalse(success)
            self.assertIn("$ invalid", output)
            self.assertNotIn("$ cd /later", output)

    def test_missing_script(self) -> None:
        output = []
        success = run_script("not_found.txt", Shell(), output.append)
        self.assertFalse(success)
        self.assertIn("Ошибка стартового скрипта", output[0])

    def test_exit_in_script(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "start.txt"
            path.write_text("exit\nls\n", encoding="utf-8")
            shell = Shell()
            output = []
            self.assertTrue(run_script(str(path), shell, output.append))
            self.assertTrue(shell.exit_requested)
            self.assertNotIn("$ ls", output)

    def test_script_stops_on_vfs_error(self) -> None:
        vfs = VirtualFileSystem.from_xml("vfs/deep.xml")
        output = []
        success = run_script(
            "scripts/vfs_all.txt", Shell(vfs), output.append
        )
        self.assertFalse(success)
        self.assertIn("$ cd /missing", output)
        self.assertNotIn("$ ls", output[-2:])


if __name__ == "__main__":
    unittest.main()
