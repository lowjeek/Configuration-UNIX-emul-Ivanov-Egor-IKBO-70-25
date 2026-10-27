import unittest

from src.emulator.parser import parse_command


class ParserTests(unittest.TestCase):
    def test_command_and_arguments(self) -> None:
        self.assertEqual(
            parse_command(" ls   -l   /home  "),
            ("ls", ["-l", "/home"]),
        )

    def test_empty_line(self) -> None:
        self.assertEqual(parse_command("  "), (None, []))


if __name__ == "__main__":
    unittest.main()
