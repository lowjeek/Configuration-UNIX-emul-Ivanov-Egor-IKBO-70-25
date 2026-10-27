import hashlib
import tempfile
import unittest
from pathlib import Path

from src.emulator.shell import Shell
from src.emulator.vfs import VfsError, VirtualFileSystem


class VfsTests(unittest.TestCase):
    def test_minimal(self) -> None:
        vfs = VirtualFileSystem.from_xml("vfs/minimal.xml")
        self.assertEqual(vfs.list_directory("/"), "")

    def test_multiple_and_binary_content(self) -> None:
        vfs = VirtualFileSystem.from_xml("vfs/multiple.xml")
        self.assertIn("home", vfs.list_directory("/"))
        node = vfs.get_node("/home/image.bin")
        self.assertEqual(node.content, bytes(range(5)))

    def test_deep_paths(self) -> None:
        vfs = VirtualFileSystem.from_xml("vfs/deep.xml")
        shell = Shell(vfs)
        self.assertFalse(shell.execute("cd /home/student").is_error)
        self.assertEqual(shell.cwd, "/home/student")
        self.assertIn("docs", shell.execute("ls").output)
        self.assertFalse(shell.execute("cd docs").is_error)
        self.assertIn("notes.txt", shell.execute("ls").output)
        self.assertFalse(shell.execute("cd ..").is_error)
        self.assertEqual(shell.cwd, "/home/student")

    def test_missing_xml(self) -> None:
        with self.assertRaises(FileNotFoundError):
            VirtualFileSystem.from_xml("vfs/absent.xml")

    def test_invalid_xml(self) -> None:
        with self.assertRaises(VfsError):
            VirtualFileSystem.from_xml("vfs/broken.xml")

    def test_bad_base64(self) -> None:
        xml = (
            '<filesystem><file name="a.bin" encoding="base64">'
            'not-valid!!</file></filesystem>'
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.xml"
            path.write_text(xml, encoding="utf-8")
            with self.assertRaises(VfsError):
                VirtualFileSystem.from_xml(str(path))

    def test_cd_rejects_file(self) -> None:
        vfs = VirtualFileSystem.from_xml("vfs/multiple.xml")
        shell = Shell(vfs)
        result = shell.execute("cd /version.txt")
        self.assertTrue(result.is_error)
        self.assertEqual(shell.cwd, "/")

    def test_ls_rejects_missing_path(self) -> None:
        vfs = VirtualFileSystem.from_xml("vfs/multiple.xml")
        result = Shell(vfs).execute("ls /nothing")
        self.assertTrue(result.is_error)

    def test_cd_too_many_arguments(self) -> None:
        vfs = VirtualFileSystem.from_xml("vfs/minimal.xml")
        self.assertTrue(Shell(vfs).execute("cd a b").is_error)

    def test_ls_rejects_option(self) -> None:
        vfs = VirtualFileSystem.from_xml("vfs/minimal.xml")
        self.assertTrue(Shell(vfs).execute("ls -l").is_error)

    def test_xml_source_is_not_modified(self) -> None:
        path = Path("vfs/deep.xml")
        before = hashlib.sha256(path.read_bytes()).digest()
        vfs = VirtualFileSystem.from_xml(str(path))
        vfs.list_directory("/home/student/docs")
        vfs.change_directory("/home/student")
        after = hashlib.sha256(path.read_bytes()).digest()
        self.assertEqual(before, after)

    def test_invalid_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.xml"
            path.write_text("<root />", encoding="utf-8")
            with self.assertRaises(VfsError):
                VirtualFileSystem.from_xml(str(path))

    def test_duplicate_names(self) -> None:
        xml = '<filesystem><dir name="x" /><dir name="x" /></filesystem>'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.xml"
            path.write_text(xml, encoding="utf-8")
            with self.assertRaises(VfsError):
                VirtualFileSystem.from_xml(str(path))


if __name__ == "__main__":
    unittest.main()
