import sys
from dataclasses import replace
import tkinter as tk
from tkinter import messagebox

from src.emulator.gui import TerminalWindow
from src.emulator.settings import load_settings
from src.emulator.shell import Shell
from src.emulator.vfs import VfsError, VirtualFileSystem


def report_error(message: str) -> int:
    print(message, file=sys.stderr)
    try:
        root = tk.Tk()
    except tk.TclError:
        return 1
    root.withdraw()
    messagebox.showerror("Ошибка запуска", message, parent=root)
    root.destroy()
    return 1


def main() -> int:
    try:
        settings = load_settings()
    except ValueError as error:
        return report_error(f"Ошибка конфигурации: {error}")
    path = settings.vfs_path or "vfs/minimal.xml"
    settings = replace(settings, vfs_path=path)
    try:
        vfs = VirtualFileSystem.from_xml(path)
    except (OSError, VfsError) as error:
        return report_error(f"Ошибка загрузки VFS: {error}")
    root = tk.Tk()
    TerminalWindow(root, Shell(vfs), settings)
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
