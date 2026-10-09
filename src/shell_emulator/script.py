"""Выполнение стартового скрипта эмулятора."""

from src.shell_emulator.messages import ERROR_PREFIX


class ScriptError(Exception):
    """Ошибка при чтении или выполнении стартового скрипта."""


def read_script_lines(path):
    """Читает строки скрипта из файла."""
    try:
        with open(path, encoding="utf-8-sig") as script_file:
            return script_file.read().splitlines()
    except OSError as exc:
        raise ScriptError(f"не удалось прочитать '{path}': {exc}") from exc


def is_skipped(line):
    """Пустые строки и комментарии (#) в скрипте пропускаются."""
    stripped = line.strip()
    return not stripped or stripped.startswith("#")


def run_script(path, prompt, handle_line):
    """Выполняет скрипт, показывая и ввод, и вывод, как в диалоге.

    Останавливается на первой ошибке и поднимает ScriptError.
    Команда exit завершает эмулятор (SystemExit проходит наружу).
    """
    lines = read_script_lines(path)
    for number, line in enumerate(lines, start=1):
        if is_skipped(line):
            continue
        print(f"{prompt}{line}")
        output = handle_line(line)
        if output is None:
            continue
        print(output)
        if output.startswith(ERROR_PREFIX):
            raise ScriptError(
                f"выполнение остановлено на строке {number}: {line.strip()}"
            )