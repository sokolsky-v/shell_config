"""Текстовые команды над файлами VFS: head, uniq."""

from itertools import groupby

from src.shell_emulator.errors import CommandError
from src.shell_emulator.fs_commands import find_node
from src.shell_emulator.vfs import Directory

DEFAULT_HEAD_LINES = 10
MIN_LINES = 0
HEAD_COUNT_OPTION = "-n"
COUNT_WIDTH = 7
REPEAT_THRESHOLD = 1
MAX_OPERANDS = 1
UNIQ_FLAGS = {"-c": "count", "-d": "repeated", "-u": "unique"}


def read_text(session, command, path):
    """Читает файл VFS как текст UTF-8."""
    node = find_node(session, command, path)
    if isinstance(node, Directory):
        raise CommandError(f"{command}: {path}: это каталог")
    try:
        return node.data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CommandError(f"{command}: {path}: двоичный файл") from exc


def _single_operand(command, operands):
    """Проверяет, что указан ровно один файл, и возвращает его."""
    if not operands:
        raise CommandError(f"{command}: не указан файл")
    if len(operands) > MAX_OPERANDS:
        raise CommandError(f"{command}: слишком много аргументов")
    return operands[0]


def _parse_line_count(value):
    """Разбирает число строк для опции -n."""
    if value is None:
        raise CommandError("head: опция -n требует число")
    try:
        count = int(value)
    except ValueError as exc:
        raise CommandError(f"head: неверное число строк: '{value}'") from exc
    if count < MIN_LINES:
        raise CommandError(f"head: неверное число строк: '{value}'")
    return count


def _parse_head_arguments(arguments):
    """Делит аргументы head на число строк и список файлов."""
    count = DEFAULT_HEAD_LINES
    operands = []
    tokens = iter(arguments)
    for token in tokens:
        if token == HEAD_COUNT_OPTION:
            count = _parse_line_count(next(tokens, None))
        elif token.startswith("-"):
            raise CommandError(f"head: неизвестная опция '{token}'")
        else:
            operands.append(token)
    return count, operands


def cmd_head(session, arguments):
    """head [-n N] файл: первые N строк файла (по умолчанию 10)."""
    count, operands = _parse_head_arguments(arguments)
    path = _single_operand("head", operands)
    lines = read_text(session, "head", path).splitlines()
    return "\n".join(lines[:count])


def _parse_uniq_arguments(arguments):
    """Делит аргументы uniq на набор опций и список файлов."""
    flags = set()
    operands = []
    for token in arguments:
        if token in UNIQ_FLAGS:
            flags.add(UNIQ_FLAGS[token])
        elif token.startswith("-"):
            raise CommandError(f"uniq: неизвестная опция '{token}'")
        else:
            operands.append(token)
    if {"repeated", "unique"} <= flags:
        raise CommandError("uniq: опции -d и -u несовместимы")
    return flags, operands


def _group_lines(text):
    """Склеивает подряд идущие одинаковые строки: (строка, повторов)."""
    return [
        (line, len(list(group)))
        for line, group in groupby(text.splitlines())
    ]


def _select_groups(groups, flags):
    """Оставляет группы согласно опциям -d (повторы) и -u (уникальные)."""
    if "repeated" in flags:
        return [g for g in groups if g[1] > REPEAT_THRESHOLD]
    if "unique" in flags:
        return [g for g in groups if g[1] <= REPEAT_THRESHOLD]
    return groups


def cmd_uniq(session, arguments):
    """uniq [-c] [-d] [-u] файл: убирает подряд идущие дубли строк."""
    flags, operands = _parse_uniq_arguments(arguments)
    path = _single_operand("uniq", operands)
    groups = _group_lines(read_text(session, "uniq", path))
    lines = []
    for line, count in _select_groups(groups, flags):
        if "count" in flags:
            line = f"{count:>{COUNT_WIDTH}} {line}"
        lines.append(line)
    return "\n".join(lines)