"""Точка входа эмулятора: настройка, VFS, стартовый скрипт и REPL."""

import sys
from functools import partial

from src.shell_emulator.commands import execute_command
from src.shell_emulator.config import ConfigError, format_debug, load_settings
from src.shell_emulator.errors import CommandError
from src.shell_emulator.messages import ERROR_PREFIX
from src.shell_emulator.parser import ParseError, parse_line
from src.shell_emulator.script import ScriptError, run_script
from src.shell_emulator.session import Session
from src.shell_emulator.vfs import Directory, Vfs, VfsError
from src.shell_emulator.vfs_loader import load_vfs

DEFAULT_VFS_NAME = "myvfs"
EXIT_COMMAND = "exit"


def build_vfs(settings):
    """Загружает VFS из XML или создаёт пустую, если путь не задан."""
    if settings.vfs_path is None:
        return Vfs(DEFAULT_VFS_NAME, Directory(""))
    return load_vfs(settings.vfs_path)


def build_prompt(vfs_name):
    """Приглашение к вводу вида 'имя_vfs> '."""
    return f"{vfs_name}> "


def handle_line(session, line):
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
        result = execute_command(session, command_name, arguments)
    except CommandError as error:
        return f"{ERROR_PREFIX} {error}"
    return result or None


def run_repl(prompt, handler):
    """Интерактивный цикл: ввод -> обработка -> вывод."""
    interactive = sys.stdin.isatty()
    while True:
        try:
            line = input(prompt)
        except EOFError:
            print()
            break
        if not interactive:
            print(line)
        try:
            output = handler(line)
        except SystemExit:
            break
        if output:
            print(output)


def start(settings):
    """Загружает VFS, выполняет стартовый скрипт и запускает REPL."""
    try:
        vfs = build_vfs(settings)
    except VfsError as error:
        print(f"{ERROR_PREFIX} VFS: {error}", file=sys.stderr)
        return 1

    handler = partial(handle_line, Session(vfs))
    prompt = build_prompt(vfs.name)

    if settings.script_path is not None:
        try:
            run_script(settings.script_path, prompt, handler)
        except ScriptError as error:
            print(f"{ERROR_PREFIX} стартовый скрипт: {error}", file=sys.stderr)
            return 1
        except SystemExit:
            return 0

    run_repl(prompt, handler)
    return 0


def main(argv=None):
    """Запуск эмулятора. Возвращает код завершения процесса."""
    try:
        settings = load_settings(argv)
    except ConfigError as error:
        print(f"{ERROR_PREFIX} конфигурация: {error}", file=sys.stderr)
        return 1

    for debug_line in format_debug(settings):
        print(debug_line)
    return start(settings)


if __name__ == "__main__":
    sys.exit(main())