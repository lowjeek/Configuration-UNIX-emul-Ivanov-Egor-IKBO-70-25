import argparse
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class Settings:
    cli_vfs: str | None
    cli_script: str | None
    config_path: str | None
    file_vfs: str | None
    file_script: str | None
    vfs_path: str | None
    script_path: str | None


def read_yaml(path: str | None) -> dict[str, str]:
    if path is None:
        return {}
    try:
        content = Path(path).read_text(encoding="utf-8")
        data = yaml.safe_load(content)
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise ValueError(f"не удалось прочитать YAML: {error}") from error
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError("YAML должен содержать словарь настроек")
    for name, value in data.items():
        if name not in {"vfs", "script"}:
            raise ValueError(f"неизвестный параметр YAML: {name}")
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"неверное значение YAML: {name}")
    return data


def load_settings(argv: list[str] | None = None) -> Settings:
    parser = argparse.ArgumentParser(description="Эмулятор UNIX")
    parser.add_argument("--vfs", help="Путь к XML-файлу VFS")
    parser.add_argument("--script", help="Путь к стартовому скрипту")
    parser.add_argument("--config", help="Путь к YAML-конфигурации")
    args = parser.parse_args(argv)
    config = read_yaml(args.config)
    file_vfs = config.get("vfs")
    file_script = config.get("script")
    return Settings(
        cli_vfs=args.vfs,
        cli_script=args.script,
        config_path=args.config,
        file_vfs=file_vfs,
        file_script=file_script,
        vfs_path=file_vfs if file_vfs is not None else args.vfs,
        script_path=(
            file_script if file_script is not None else args.script
        ),
    )
