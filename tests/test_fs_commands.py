"""Тесты путей и команд ls, cd, pwd."""

import pytest

from src.shell_emulator.commands import execute_command
from src.shell_emulator.errors import CommandError
from src.shell_emulator.vfs import VfsError, lookup, normalize


def run(session, line_command, *arguments):
    return execute_command(session, line_command, list(arguments))


def test_normalize_absolute_and_relative():
    assert normalize(["a"], "/b/c") == ["b", "c"]
    assert normalize(["a"], "b/c") == ["a", "b", "c"]


def test_normalize_dots_and_slashes():
    assert normalize(["a", "b"], "../c//./d/") == ["a", "c", "d"]


def test_normalize_cannot_go_above_root():
    assert normalize([], "../../x") == ["x"]


def test_lookup_errors(session):
    with pytest.raises(VfsError):
        lookup(session.vfs, ["nope"])
    with pytest.raises(VfsError):
        lookup(session.vfs, ["readme.txt", "x"])


def test_ls_root_sorted(session):
    names = run(session, "ls").splitlines()
    assert names == [
        "data.bin", "docs", "dups.txt", "empty", "readme.txt",
    ]


def test_ls_path_and_empty_dir(session):
    assert run(session, "ls", "docs").splitlines() == ["deep", "notes.txt"]
    assert run(session, "ls", "empty") == ""


def test_ls_long_format(session):
    lines = run(session, "ls", "-l").splitlines()
    assert lines[0] == "-        6 data.bin"
    assert lines[1] == "d        - docs"


def test_ls_single_file(session):
    assert run(session, "ls", "docs/deep/deeper/file.txt") == (
        "docs/deep/deeper/file.txt"
    )


@pytest.mark.parametrize(
    "arguments",
    [["nope"], ["-x"], ["a", "b"], ["readme.txt/x"]],
)
def test_ls_errors(session, arguments):
    with pytest.raises(CommandError):
        run(session, "ls", *arguments)


def test_cd_and_pwd(session):
    assert run(session, "pwd") == "/"
    run(session, "cd", "docs/deep")
    assert run(session, "pwd") == "/docs/deep"
    run(session, "cd", "..")
    assert run(session, "pwd") == "/docs"
    run(session, "cd")
    assert run(session, "pwd") == "/"


def test_cd_absolute_and_relative_ls(session):
    run(session, "cd", "/docs")
    assert run(session, "ls").splitlines() == ["deep", "notes.txt"]
    run(session, "cd", "deep/deeper")
    assert run(session, "ls") == "file.txt"


@pytest.mark.parametrize("arguments", [["nope"], ["readme.txt"], ["a", "b"]])
def test_cd_errors_keep_position(session, arguments):
    run(session, "cd", "docs")
    with pytest.raises(CommandError):
        run(session, "cd", *arguments)
    assert run(session, "pwd") == "/docs"


def test_pwd_rejects_arguments(session):
    with pytest.raises(CommandError):
        run(session, "pwd", "x")