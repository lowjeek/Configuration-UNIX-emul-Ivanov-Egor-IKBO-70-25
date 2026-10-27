import tempfile
import unittest
from pathlib import Path

from src.emulator.settings import load_settings, read_yaml


class SettingsTests(unittest.TestCase):
    def test_cli_parameters(self) -> None:
        settings = load_settings(["--vfs", "a.xml", "--script", "a.txt"])
        self.assertEqual(settings.vfs_path, "a.xml")
        self.assertEqual(settings.script_path, "a.txt")

    def test_yaml_overrides_cli(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.yaml"
            path.write_text(
                "vfs: correct.xml\nscript: correct.txt\n",
                encoding="utf-8",
            )
            settings = load_settings([
                "--vfs", "wrong.xml",
                "--script", "wrong.txt",
                "--config", str(path),
            ])
            self.assertEqual(settings.vfs_path, "correct.xml")
            self.assertEqual(settings.script_path, "correct.txt")

    def test_missing_yaml(self) -> None:
        with self.assertRaises(ValueError):
            read_yaml("this_file_does_not_exist.yaml")

    def test_bad_yaml_type(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.yaml"
            path.write_text("- wrong\n- type\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                read_yaml(str(path))


if __name__ == "__main__":
    unittest.main()
