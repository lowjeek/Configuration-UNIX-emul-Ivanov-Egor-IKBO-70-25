from collections.abc import Callable
from pathlib import Path

from src.emulator.shell import Shell


def run_script(
    path: str,
    shell: Shell,
    emit: Callable[[str], None],
) -> bool:
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        emit(f"Ошибка стартового скрипта: {error}")
        return False
    for number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line:
            continue
        emit(f"$ {line}")
        result = shell.execute(line)
        if result.output:
            emit(result.output)
        if result.is_error:
            emit(f"Ошибка стартового скрипта, строка {number}.")
            emit("Выполнение остановлено.")
            return False
        if result.should_exit:
            return True
    return True
