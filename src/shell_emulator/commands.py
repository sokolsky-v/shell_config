"""Команды эмулятора и их диспетчер."""

from src.shell_emulator.errors import CommandError


def cmd_ls(session, arguments):
    """Заглушка ls: печатает имя команды и аргументы."""
    return f"CMD: ls ARGS: {list(arguments)}"


def cmd_cd(session, arguments):
    """Заглушка cd: печатает имя команды и аргументы."""
    return f"CMD: cd ARGS: {list(arguments)}"


def cmd_vfs_info(session, arguments):
    """Служебная команда vfs-info: сведения о загруженной VFS."""
    if arguments:
        raise CommandError("vfs-info: команда не принимает аргументов")
    stats = session.vfs.stats()
    return "\n".join(
        [
            f"VFS: {session.vfs.name}",
            f"Каталогов: {stats.directories}",
            f"Файлов: {stats.files}",
            f"Глубина: {stats.depth}",
        ]
    )


COMMAND_TABLE = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "vfs-info": cmd_vfs_info,
}


def execute_command(session, command_name, arguments):
    """Находит команду в таблице и выполняет её."""
    handler = COMMAND_TABLE.get(command_name)
    if handler is None:
        raise CommandError(f"неизвестная команда: {command_name}")
    return handler(session, arguments)