"""Тесты диспетчера команд и обработчика строк."""

import pytest

from src.shell_emulator.commands import execute_command
from src.shell_emulator.errors import CommandError
from src.shell_emulator.main import handle_line


def test_vfs_info(session):
    lines = execute_command(session, "vfs-info", []).splitlines()
    assert lines == ["VFS: demo", "Каталогов: 4", "Файлов: 5", "Глубина: 4"]


def test_vfs_info_rejects_arguments(session):
    with pytest.raises(CommandError):
        execute_command(session, "vfs-info", ["x"])


def test_unknown_command_raises(session):
    with pytest.raises(CommandError):
        execute_command(session, "foobar", [])


def test_handle_line_unknown_command(session):
    output = handle_line(session, "foobar")
    assert output == "Ошибка: неизвестная команда: foobar"


def test_handle_line_empty(session):
    assert handle_line(session, "   ") is None


def test_handle_line_command_without_output(session):
    assert handle_line(session, "cd docs") is None


def test_handle_line_parse_error(session):
    assert handle_line(session, 'cd "x').startswith("Ошибка:")


def test_handle_line_exit(session):
    with pytest.raises(SystemExit):
        handle_line(session, "exit")