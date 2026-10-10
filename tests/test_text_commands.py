"""Тесты команд head и uniq."""

import pytest

from src.shell_emulator.commands import execute_command
from src.shell_emulator.errors import CommandError


def run(session, command, *arguments):
    return execute_command(session, command, list(arguments))


def test_head_default_ten_lines(session):
    lines = run(session, "head", "docs/notes.txt").splitlines()
    assert lines == [str(number) for number in range(1, 11)]


def test_head_n_option(session):
    assert run(session, "head", "-n", "3", "docs/notes.txt") == "1\n2\n3"


def test_head_n_larger_than_file(session):
    assert run(session, "head", "-n", "50", "readme.txt") == "Привет\nмир"


def test_head_zero_lines(session):
    assert run(session, "head", "-n", "0", "readme.txt") == ""


def test_head_uses_current_directory(session):
    run(session, "cd", "docs")
    assert run(session, "head", "-n", "1", "notes.txt") == "1"


@pytest.mark.parametrize(
    "arguments",
    [
        [],
        ["nope.txt"],
        ["docs"],
        ["data.bin"],
        ["-n"],
        ["-n", "abc", "readme.txt"],
        ["-n", "-2", "readme.txt"],
        ["-x", "readme.txt"],
        ["readme.txt", "dups.txt"],
    ],
)
def test_head_errors(session, arguments):
    with pytest.raises(CommandError):
        run(session, "head", *arguments)


def test_uniq_default(session):
    assert run(session, "uniq", "dups.txt").splitlines() == [
        "a", "b", "c", "a",
    ]


def test_uniq_count(session):
    lines = run(session, "uniq", "-c", "dups.txt").splitlines()
    assert lines[0] == "      2 a"
    assert lines[1] == "      3 b"


def test_uniq_repeated_only(session):
    assert run(session, "uniq", "-d", "dups.txt").splitlines() == ["a", "b"]


def test_uniq_unique_only(session):
    assert run(session, "uniq", "-u", "dups.txt").splitlines() == ["c", "a"]


def test_uniq_count_with_repeated(session):
    lines = run(session, "uniq", "-c", "-d", "dups.txt").splitlines()
    assert lines == ["      2 a", "      3 b"]


@pytest.mark.parametrize(
    "arguments",
    [
        [],
        ["nope.txt"],
        ["docs"],
        ["data.bin"],
        ["-d", "-u", "dups.txt"],
        ["-x", "dups.txt"],
        ["dups.txt", "readme.txt"],
    ],
)
def test_uniq_errors(session, arguments):
    with pytest.raises(CommandError):
        run(session, "uniq", *arguments)