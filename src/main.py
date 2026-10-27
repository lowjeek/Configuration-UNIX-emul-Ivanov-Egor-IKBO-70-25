import tkinter as tk

from src.emulator.gui import TerminalWindow
from src.emulator.shell import Shell


def main() -> None:
    root = tk.Tk()
    TerminalWindow(root, Shell())
    root.mainloop()


if __name__ == "__main__":
    main()
