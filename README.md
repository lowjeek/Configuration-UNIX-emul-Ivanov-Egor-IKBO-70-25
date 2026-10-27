# Эмулятор UNIX-оболочки — вариант №5

Разработка по дисциплине «Конфигурационное управление».
Реализованы этапы 1–3.

## Возможности

- GUI терминал на Tkinter.
- Заголовок `Эмулятор - [username@hostname]` из реальных данных ОС.
- Парсер по пробелам, команды `ls`, `cd`, `exit` и обработка ошибок.
- Параметры запуска `--vfs`, `--script`, `--config`.
- YAML имеет приоритет над командной строкой.
- Стартовый скрипт показывается как диалог и останавливается при ошибке.
- Виртуальная файловая система XML целиком загружается в память.
- Бинарные файлы декодируются из base64 в байты в памяти.
- `ls` и `cd` работают с директориями VFS.
- Физический файл XML при работе не изменяется.

## Требования

Python 3.10+ с Tkinter, PyYAML.

```bash
python -m pip install -r requirements.txt
```

## Запуск

Из корня репозитория в Windows:

```powershell
.\run.bat --vfs vfs/deep.xml --script scripts/vfs_deep.txt
```

В Linux/macOS:

```bash
bash run.sh --vfs vfs/deep.xml --script scripts/vfs_deep.txt
```

С настройками из YAML:

```bash
python -m src.main --config configs/deep.yaml
```

Если параметр `--vfs` не задан и YAML не задаёт путь VFS,
используется `vfs/minimal.xml`.

## Конфигурация

Пример `configs/deep.yaml`:

```yaml
vfs: vfs/deep.xml
script: scripts/vfs_deep.txt
```

`--vfs` — физический путь к XML, `--script` — путь к текстовому
стартовому скрипту, `--config` — путь к YAML.

Пути относительны корневой папке при запуске из корня репозитория.
Для `vfs` и `script` YAML имеет приоритет над CLI.
В окне выводятся исходные и итоговые параметры.

## Формат VFS

Корневой элемент `<filesystem>`. Папка — `<dir name="...">`,
файл — `<file name="..." encoding="text">` или `encoding="base64"`.
Выполняется проверка корневого элемента, тегов, имён, дубликатов,
кодировок и содержимого base64.

Никакой распаковки на диск и модификации источника XML нет.

## Команды

- `ls` — элементы текущей папки.
- `ls /путь` — элементы папки либо имя файла.
- `cd /путь` — переход в папку.
- `cd ..` — переход к родителю.
- `cd` — переход в `/`.
- `exit` — завершение работы эмулятора.

Пока нет обработки флагов `ls` и чтения содержимого файла
в интерфейсе: расширение предусмотрено следующими этапами.

## Скрипты реальной ОС

Windows: `scripts/test_cli.bat`, `scripts/test_priority.bat`,
`scripts/test_error.bat`, `scripts/test_minimal.bat`,
`scripts/test_multiple.bat`, `scripts/test_deep.bat`,
`scripts/test_missing.bat`, `scripts/test_broken.bat`.

Linux/macOS: файлы с теми же именами и расширением `.sh`.

Все скрипты ОС запускают приложение с тремя параметрами.
Варианты VFS: минимальный, несколько файлов, три уровня папок.
Проверяются также отсутствующий файл и повреждённый XML.

## Стартовые скрипты

- `scripts/success.txt` — демонстрация заглушек этапа 2.
- `scripts/fail.txt` — остановка на неизвестной команде.
- `scripts/vfs_basic.txt` — команды `ls`, `cd`.
- `scripts/vfs_deep.txt` — абсолютные и относительные пути.
- `scripts/vfs_all.txt` — разные режимы, ошибка в конце, остановка.
- `scripts/vfs_exit.txt` — команда `exit` в сценарии.
- `scripts/vfs_bad_ls.txt` — недопустимый флаг `ls`.
- `scripts/vfs_bad_cd.txt` — лишний аргумент `cd`.
- `scripts/vfs_bad_unknown.txt` — неизвестная команда.
- `scripts/vfs_error.txt` — ошибка обращения к отсутствующей папке.

Пример ошибки скрипта:

```bash
python -m src.main --vfs vfs/deep.xml --script scripts/vfs_error.txt
```

## Тесты

```bash
python -m unittest discover -s tests -v
```

## Ограничения текущего этапа

Парсер намеренно разделяет слова только пробелами, без кавычек.
Поддерживается базовый `ls` и `cd`; команды `rev`, `echo`, `date`
будут реализованы на этапе 4, `chmod` — на этапе 5.
