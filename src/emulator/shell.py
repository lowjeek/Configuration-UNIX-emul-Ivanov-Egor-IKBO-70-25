from dataclasses import dataclass

from src.emulator.parser import parse_command


@dataclass(frozen=True)
class CommandResult:
    output: str = ""
    is_error: bool = False
    should_exit: bool = False


class Shell:
    def __init__(self) -> None:
        self.exit_requested = False

    def execute(self, line: str) -> CommandResult:
        name, args = parse_command(line)
        if name is None:
            return CommandResult()
        commands = {
            "ls": self._ls,
            "cd": self._cd,
            "exit": self._exit,
        }
        handler = commands.get(name)
        if handler is None:
            return CommandResult(
                f"{name}: команда не найдена", is_error=True
            )
        return handler(args)

    def _ls(self, args: list[str]) -> CommandResult:
        return CommandResult(f"ls: аргументы {args}")

    def _cd(self, args: list[str]) -> CommandResult:
        return CommandResult(f"cd: аргументы {args}")

    def _exit(self, args: list[str]) -> CommandResult:
        if args:
            return CommandResult(
                "exit: аргументы не допускаются", is_error=True
            )
        self.exit_requested = True
        return CommandResult(
            "Завершение эмулятора", should_exit=True
        )
