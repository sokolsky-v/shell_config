"""Команды изменения VFS (только в памяти): touch, mv."""

from src.shell_emulator.errors import CommandError
from src.shell_emulator.vfs import VfsError, create_file, move_node, normalize

NO_CLOBBER_OPTION = "-n"
MV_OPERANDS = 2


def _split_options(command, arguments, known_options):
    """Делит аргументы на набор известных опций и список операндов."""
    options = set()
    operands = []
    for token in arguments:
        if token in known_options:
            options.add(token)
        elif token.startswith("-"):
            raise CommandError(f"{command}: неизвестная опция '{token}'")
        else:
            operands.append(token)
    return options, operands


def cmd_touch(session, arguments):
    """touch файл...: создаёт пустые файлы (существующие не меняет)."""
    _, operands = _split_options("touch", arguments, ())
    if not operands:
        raise CommandError("touch: не указан файл")
    for path in operands:
        try:
            create_file(session.vfs, normalize(session.cwd, path))
        except VfsError as exc:
            raise CommandError(f"touch: {path}: {exc}") from exc
    return ""


def _follow_cwd(session, src, final):
    """Если текущий каталог переехал вместе с каталогом, правим cwd."""
    if session.cwd[: len(src)] == src:
        session.cwd = final + session.cwd[len(src):]


def cmd_mv(session, arguments):
    """mv [-n] источник назначение: перемещение и переименование."""
    options, operands = _split_options(
        "mv", arguments, (NO_CLOBBER_OPTION,)
    )
    if len(operands) != MV_OPERANDS:
        raise CommandError("mv: нужно указать источник и назначение")
    source, target = operands
    src = normalize(session.cwd, source)
    try:
        final = move_node(
            session.vfs,
            src,
            normalize(session.cwd, target),
            overwrite=NO_CLOBBER_OPTION not in options,
        )
    except VfsError as exc:
        raise CommandError(f"mv: {source} -> {target}: {exc}") from exc
    if final is not None:
        _follow_cwd(session, src, final)
    return ""