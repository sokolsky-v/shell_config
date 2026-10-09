# Эмулятор командной строки. Вариант №23

## Общее описание

«Конфигурационное управление»
Эмулятор командной строки UNIX-подобной ОС на Python.

Этапы разработки:
- Этап 1. REPL: разбор ввода, раскрытие переменных окружения, заглушки `ls`, `cd`, команда `exit`.
- Этап 2. Конфигурация: параметры командной строки, XML-конфиг, стартовый скрипт.
- Этап 3. Подключение VFS (загрузка из XML, работа только в памяти).
- Этап 4. Команды `ls`, `cd`, `uniq`, `pwd`, `head`.
- Этап 5. Команды изменения VFS: `touch`, `mv`.

## Описание функций и настроек

### Команды

| Команда | Описание |
|---|---|
| `ls [args...]` | Заглушка: печатает имя команды и аргументы |
| `cd [args...]` | Заглушка: печатает имя команды и аргументы |
| `exit` | Завершает работу эмулятора |

Переменные окружения реальной ОС раскрываются в аргументах (например, `$USERPROFILE`
на Windows, `$HOME` на Linux/macOS). Кавычки группируют слова: `cd "my folder"`.

### Параметры командной строки

| Параметр | Описание |
|---|---|
| `--vfs ПУТЬ` | Путь к физическому расположению VFS |
| `--script ПУТЬ` | Путь к стартовому скрипту |
| `--config ПУТЬ` | Путь к XML-файлу конфигурации |

При запуске эмулятор выводит отладочную строку для каждого параметра
(`[debug] ...`). Незаданный параметр показывается как `<не задан>`.

### Конфигурационный файл (XML)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config>
    <vfs_path>examples/vfs/from_config.xml</vfs_path>
    <startup_script>examples/startup/ok.txt</startup_script>
</config>
```

**Приоритет:** значения из командной строки главнее значений из файла.
Если параметр не задан в командной строке, берётся значение из файла.

### Стартовый скрипт

Текстовый файл, одна команда эмулятора в строке. Строки, начинающиеся с `#`,
и пустые строки пропускаются. При выполнении на экране показывается и ввод
(с приглашением), и вывод, как в живом диалоге. Скрипт **останавливается на
первой ошибке**. Команда `exit` в скрипте завершает эмулятор.

### Обработка ошибок

| Ситуация | Сообщение | Код завершения |
|---|---|---|
| Конфиг не найден / не открывается | `Ошибка: конфигурация: не удалось открыть ...` | 1 |
| Конфиг не является корректным XML | `Ошибка: конфигурация: некорректный XML ...` | 1 |
| Корневой тег конфига не `<config>` | `Ошибка: конфигурация: корневой тег ...` | 1 |
| Скрипт не найден | `Ошибка: стартовый скрипт: не удалось прочитать ...` | 1 |
| Ошибка команды в скрипте | `Ошибка: стартовый скрипт: выполнение остановлено на строке N` | 1 |
| Неизвестная команда в интерактивном режиме | `Ошибка: неизвестная команда: ...` (диалог продолжается) | — |

## Сборка и запуск

Требуется Python 3.10+.

```
pip install -r requirements-dev.txt
python -m src.shell_emulator.main
python -m pytest tests
```

Скрипты проверки параметров (Windows, запускать из корня проекта):

```
scripts\test_cli_params.bat
scripts\test_config_file.bat
scripts\test_errors.bat
```

## Примеры использования

Интерактивный режим:

```
> python -m src.shell_emulator.main
[debug] Параметры запуска:
[debug]   vfs    = <не задан>
[debug]   script = <не задан>
[debug]   config = <не задан>
myvfs> ls firienodv
CMD: ls ARGS: ['firienodv']
myvfs> foobar
Ошибка: неизвестная команда: foobar
myvfs> exit
```

Стартовый скрипт:

```
> python -m src.shell_emulator.main --script examples/startup/ok.txt
[debug] Параметры запуска:
[debug]   vfs    = <не задан>
[debug]   script = examples/startup/ok.txt
[debug]   config = <не задан>
myvfs> ls /home
CMD: ls ARGS: ['/home']
myvfs> cd $USERPROFILE
CMD: cd ARGS: ['C:\\Users\\sokol']
myvfs> ls -la
CMD: ls ARGS: ['-la']
myvfs> exit
```

Приоритет командной строки над конфигом:

```
> python -m src.shell_emulator.main --config examples/configs/config_ok.xml --vfs cli.xml
[debug] Параметры запуска:
[debug]   vfs    = cli.xml
[debug]   script = examples/startup/ok.txt
[debug]   config = examples/configs/config_ok.xml
```

Ошибка в стартовом скрипте (остановка на первой ошибке):

```
> python -m src.shell_emulator.main --script examples/startup/with_error.txt
myvfs> ls /home
CMD: ls ARGS: ['/home']
myvfs> foobar
Ошибка: неизвестная команда: foobar
Ошибка: стартовый скрипт: выполнение остановлено на строке 3: foobar
```

Ошибка чтения конфига:

```
> python -m src.shell_emulator.main --config examples/configs/config_broken.xml
Ошибка: конфигурация: некорректный XML в 'examples/configs/config_broken.xml': mismatched tag: line 4, column 2
```