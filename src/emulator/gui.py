import getpass
import socket
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from src.emulator.shell import Shell


class TerminalWindow:
    def __init__(self, root: tk.Tk, shell: Shell) -> None:
        self.root = root
        self.shell = shell
        user = getpass.getuser()
        host = socket.gethostname()
        self.prompt = f"{user}@{host}:~$"
        self.root.title(f"Эмулятор - [{user}@{host}]")
        self.root.geometry("820x500")
        self.root.configure(bg="#171b24")
        self.output = ScrolledText(
            root,
            bg="#171b24",
            fg="#e7eaf0",
            insertbackground="white",
            font=("Consolas", 12),
            wrap=tk.WORD,
            state=tk.DISABLED,
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=12, pady=(12, 4))
        self.input = tk.Entry(
            root,
            bg="#282f3d",
            fg="#ffffff",
            insertbackground="white",
            font=("Consolas", 12),
            relief=tk.FLAT,
        )
        self.input.pack(fill=tk.X, padx=12, pady=(4, 12), ipady=8)
        self.input.bind("<Return>", self.on_submit)
        self.input.focus_set()
        self.append("Эмулятор UNIX. Команды: ls, cd, exit")

    def append(self, value: str) -> None:
        if not value:
            return
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, value + "\n")
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)

    def on_submit(self, event: object = None) -> None:
        line = self.input.get()
        self.input.delete(0, tk.END)
        self.append(f"{self.prompt} {line}")
        result = self.shell.execute(line)
        self.append(result.output)
        if result.should_exit:
            self.input.configure(state=tk.DISABLED)
            self.root.after(100, self.root.destroy)
