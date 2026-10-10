"""Команды эмулятора и их диспетчер."""

from src.shell_emulator.errors import CommandError
from src.shell_emulator.fs_commands import cmd_cd, cmd_ls, cmd_pwd
from src.shell_emulator.text_commands import cmd_head, cmd_uniq


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
    "pwd": cmd_pwd,
    "head": cmd_head,
    "uniq": cmd_uniq,
    "vfs-info": cmd_vfs_info,
}


def execute_command(session, command_name, arguments):
    """Находит команду в таблице и выполняет её."""
    handler = COMMAND_TABLE.get(command_name)
    if handler is None:
        raise CommandError(f"неизвестная команда: {command_name}")
    return handler(session, arguments)