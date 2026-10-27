import unittest

from src.emulator.shell import Shell


class ShellTests(unittest.TestCase):
    def setUp(self) -> None:
        self.shell = Shell()

    def test_ls_stub(self) -> None:
        result = self.shell.execute("ls -l /tmp")
        self.assertEqual(result.output, "ls: аргументы ['-l', '/tmp']")

    def test_cd_stub(self) -> None:
        result = self.shell.execute("cd /home")
        self.assertEqual(result.output, "cd: аргументы ['/home']")

    def test_unknown_command(self) -> None:
        result = self.shell.execute("incorrect")
        self.assertTrue(result.is_error)
        self.assertIn("команда не найдена", result.output)

    def test_invalid_exit_arguments(self) -> None:
        result = self.shell.execute("exit 1")
        self.assertTrue(result.is_error)
        self.assertFalse(self.shell.exit_requested)

    def test_exit(self) -> None:
        result = self.shell.execute("exit")
        self.assertTrue(result.should_exit)
        self.assertTrue(self.shell.exit_requested)


if __name__ == "__main__":
    unittest.main()
