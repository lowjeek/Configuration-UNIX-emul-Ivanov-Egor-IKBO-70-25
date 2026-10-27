import sys
import tkinter as tk

from src.emulator.gui import TerminalWindow
from src.emulator.settings import load_settings
from src.emulator.shell import Shell


def main() -> int:
    try:
        settings = load_settings()
    except ValueError as error:
        print(f"Ошибка конфигурации: {error}", file=sys.stderr)
        return 1
    root = tk.Tk()
    TerminalWindow(root, Shell(), settings)
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
