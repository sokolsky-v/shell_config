"""Команды навигации по VFS: ls, cd, pwd."""

from src.shell_emulator.errors import CommandError
from src.shell_emulator.vfs import Directory, VfsError, lookup, normalize

LONG_OPTION = "-l"
NO_SIZE = "-"
SIZE_WIDTH = 8
MAX_PATHS = 1


def find_node(session, command, path):
    """Находит узел VFS по пути относительно текущего каталога."""
    try:
        return lookup(session.vfs, normalize(session.cwd, path))
    except VfsError as exc:
        raise CommandError(f"{command}: {path}: {exc}") from exc


def _split_ls_arguments(arguments):
    """Делит аргументы ls на признак -l и список путей."""
    long_format = False
    paths = []
    for token in arguments:
        if token == LONG_OPTION:
            long_format = True
        elif token.startswith("-"):
            raise CommandError(f"ls: неизвестная опция '{token}'")
        else:
            paths.append(token)
    if len(paths) > MAX_PATHS:
        raise CommandError("ls: слишком много аргументов")
    return long_format, paths


def _format_entry(node, label, long_format):
    """Формирует строку вывода ls для одного узла."""
    if not long_format:
        return label
    if isinstance(node, Directory):
        return f"d {NO_SIZE:>{SIZE_WIDTH}} {label}"
    return f"- {len(node.data):>{SIZE_WIDTH}} {label}"


def cmd_ls(session, arguments):
    """ls [-l] [путь]: содержимое каталога или сведения о файле."""
    long_format, paths = _split_ls_arguments(arguments)
    path = paths[0] if paths else "."
    node = find_node(session, "ls", path)
    if not isinstance(node, Directory):
        return _format_entry(node, path, long_format)
    lines = [
        _format_entry(node.children[name], name, long_format)
        for name in sorted(node.children)
    ]
    return "\n".join(lines)


def cmd_cd(session, arguments):
    """cd [путь]: переход в каталог (без аргумента - в корень)."""
    if len(arguments) > MAX_PATHS:
        raise CommandError("cd: слишком много аргументов")
    path = arguments[0] if arguments else "/"
    node = find_node(session, "cd", path)
    if not isinstance(node, Directory):
        raise CommandError(f"cd: {path}: не является каталогом")
    session.cwd = normalize(session.cwd, path)
    return ""


def cmd_pwd(session, arguments):
    """pwd: печатает путь текущего каталога."""
    if arguments:
        raise CommandError("pwd: команда не принимает аргументов")
    return "/" + "/".join(session.cwd)