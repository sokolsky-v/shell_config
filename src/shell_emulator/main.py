"""Точка входа эмулятора: настройка, стартовый скрипт и REPL."""

import sys

from src.shell_emulator.commands import (
    UnknownCommandError,
    execute_stub_command,
)
from src.shell_emulator.config import ConfigError, format_debug, load_settings
from src.shell_emulator.messages import ERROR_PREFIX
from src.shell_emulator.parser import ParseError, parse_line
from src.shell_emulator.script import ScriptError, run_script

DEFAULT_VFS_NAME = "myvfs"
EXIT_COMMAND = "exit"


def build_prompt(vfs_name):
    """Приглашение к вводу вида 'имя_vfs> '."""
    return f"{vfs_name}> "


def handle_line(line):
    """Обрабатывает одну строку; возвращает текст вывода или None."""
    try:
        command_name, arguments = parse_line(line)
    except ParseError as error:
        return f"{ERROR_PREFIX} {error}"

    if not command_name:
        return None
    if command_name == EXIT_COMMAND:
        raise SystemExit(0)

    try:
        return execute_stub_command(command_name, arguments)
    except UnknownCommandError:
        return f"{ERROR_PREFIX} неизвестная команда: {command_name}"


def run_repl(prompt):
    """Интерактивный цикл: ввод -> обработка -> вывод."""
    while True:
        try:
            line = input(prompt)
        except EOFError:
            break
        try:
            output = handle_line(line)
        except SystemExit:
            break
        if output is not None:
            print(output)


def main(argv=None):
    """Запуск эмулятора. Возвращает код завершения процесса."""
    try:
        settings = load_settings(argv)
    except ConfigError as error:
        print(f"{ERROR_PREFIX} конфигурация: {error}", file=sys.stderr)
        return 1

    for debug_line in format_debug(settings):
        print(debug_line)

    prompt = build_prompt(DEFAULT_VFS_NAME)

    if settings.script_path is not None:
        try:
            run_script(settings.script_path, prompt, handle_line)
        except ScriptError as error:
            print(f"{ERROR_PREFIX} стартовый скрипт: {error}", file=sys.stderr)
            return 1
        except SystemExit:
            return 0

    run_repl(prompt)
    return 0


if __name__ == "__main__":
    sys.exit(main())