from src.shell_emulator.commands import (
    execute_stub_command,
    UnknownCommandError,
)
from src.shell_emulator.parser import parse_line, ParseError

DEFAULT_VFS_NAME = "myvfs"
EXIT_COMMAND = "exit"


def build_prompt(vfs_name):
    return f"{vfs_name}> "


def handle_line(line):
    try:
        command_name, arguments = parse_line(line)
    except ParseError as error:
        return f"Ошибка: {error}"

    if not command_name:
        return None
    if command_name == EXIT_COMMAND:
        raise SystemExit(0)

    try:
        return execute_stub_command(command_name, arguments)
    except UnknownCommandError:
        return f"Ошибка: неизвестная команда: {command_name}"


def run_repl(vfs_name=DEFAULT_VFS_NAME):
    prompt = build_prompt(vfs_name)
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


if __name__ == "__main__":
    run_repl()