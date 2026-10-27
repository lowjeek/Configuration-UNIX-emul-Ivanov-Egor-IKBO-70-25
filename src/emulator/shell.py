from dataclasses import dataclass

from src.emulator.parser import parse_command
from src.emulator.vfs import VfsError, VirtualFileSystem


@dataclass(frozen=True)
class CommandResult:
    output: str = ""
    is_error: bool = False
    should_exit: bool = False


class Shell:
    def __init__(self, vfs: VirtualFileSystem | None = None) -> None:
        self.vfs = vfs
        self.cwd = "/"
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
            return CommandResult(f"{name}: команда не найдена", True)
        return handler(args)

    def _ls(self, args: list[str]) -> CommandResult:
        if len(args) > 1:
            return CommandResult("ls: слишком много аргументов", True)
        if args and args[0].startswith("-"):
            return CommandResult("ls: неизвестный параметр", True)
        if self.vfs is None:
            return CommandResult("ls: VFS не загружена", True)
        try:
            return CommandResult(
                self.vfs.list_directory(args[0] if args else ".", self.cwd)
            )
        except VfsError as error:
            return CommandResult(f"ls: {error}", True)

    def _cd(self, args: list[str]) -> CommandResult:
        if len(args) > 1:
            return CommandResult("cd: слишком много аргументов", True)
        if self.vfs is None:
            return CommandResult("cd: VFS не загружена", True)
        target = args[0] if args else "/"
        try:
            self.cwd = self.vfs.change_directory(target, self.cwd)
        except VfsError as error:
            return CommandResult(f"cd: {error}", True)
        return CommandResult()

    def _exit(self, args: list[str]) -> CommandResult:
        if args:
            return CommandResult("exit: аргументы не допускаются", True)
        self.exit_requested = True
        return CommandResult("Завершение эмулятора", should_exit=True)
