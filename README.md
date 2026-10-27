# Эмулятор UNIX-оболочки — вариант №5

Проект по дисциплине «Конфигурационное управление».

## Возможности

- Графический терминал на Tkinter.
- Заголовок `Эмулятор - [username@hostname]` из данных ОС.
- Парсер по пробелам.
- Заглушки `ls`, `cd`; команда `exit`; сообщения об ошибках.
- Параметры запуска `--vfs`, `--script`, `--config`.
- YAML-конфигурация с приоритетом над аргументами командной строки.
- Стартовые скрипты с выводом команд и остановкой на первой ошибке.
- Отладочный вывод аргументов, YAML и итоговых настроек.

## Подготовка

Требуется Python 3.10+, Tkinter и PyYAML.

```bash
python -m pip install -r requirements.txt
```

## Запуск

Windows:

```powershell
.\run.bat --config configs/override.yaml
```

Linux/macOS:

```bash
bash run.sh --config configs/override.yaml
```

Прямое указание параметров:

```bash
python -m src.main --vfs vfs/minimal.xml --script scripts/success.txt
```

## Примеры приоритетов

```bash
python -m src.main --vfs vfs/missing.xml --script scripts/fail.txt --config configs/override.yaml
```

Должны использоваться `vfs/minimal.xml` и `scripts/success.txt`.

## Скрипты ОС

Windows: `scripts/test_cli.bat`, `scripts/test_priority.bat`,
`scripts/test_error.bat`.

Linux/macOS: аналогичные `.sh`.

Каждый вызывает эмулятор с тремя поддерживаемыми параметрами.

## Тесты

```bash
python -m unittest discover -s tests -v
```

## Режимы и ошибки

В окне можно проверить `ls`, `cd /home`, `exit 1`, `unknown`, `exit`.
Стартовый скрипт `scripts/fail.txt` прекращает выполнение на второй строке.
На втором этапе путь VFS только считывается и отображается; загрузка XML
будет подключена на третьем этапе.
