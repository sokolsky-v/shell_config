"""Тесты команд touch и mv (изменения только в памяти)."""

import pytest

from src.shell_emulator.commands import execute_command
from src.shell_emulator.errors import CommandError
from src.shell_emulator.vfs import Directory, File


def run(session, command, *arguments):
    return execute_command(session, command, list(arguments))


def names(session, path="."):
    return run(session, "ls", path).splitlines()


def test_touch_creates_empty_file(session):
    run(session, "touch", "new.txt")
    assert "new.txt" in names(session)
    assert session.vfs.root.children["new.txt"] == File("new.txt", b"")


def test_touch_in_subdirectory_and_absolute(session):
    run(session, "touch", "docs/a.txt", "/empty/b.txt")
    assert "a.txt" in names(session, "docs")
    assert names(session, "empty") == ["b.txt"]


def test_touch_several_files(session):
    run(session, "touch", "x1", "x2", "x3")
    assert {"x1", "x2", "x3"} <= set(names(session))


def test_touch_existing_file_keeps_content(session):
    run(session, "touch", "readme.txt")
    data = session.vfs.root.children["readme.txt"].data
    assert data.decode("utf-8") == "Привет\nмир\n"


def test_touch_existing_directory_is_ok(session):
    run(session, "touch", "docs")
    assert isinstance(session.vfs.root.children["docs"], Directory)


def test_touch_relative_to_cwd(session):
    run(session, "cd", "docs")
    run(session, "touch", "local.txt")
    assert "local.txt" in names(session)


@pytest.mark.parametrize(
    "arguments",
    [[], ["-x", "a"], ["nope/a.txt"], ["readme.txt/a.txt"]],
)
def test_touch_errors(session, arguments):
    with pytest.raises(CommandError):
        run(session, "touch", *arguments)


def test_mv_renames_file(session):
    run(session, "mv", "readme.txt", "hello.txt")
    assert "readme.txt" not in names(session)
    assert "hello.txt" in names(session)
    assert session.vfs.root.children["hello.txt"].name == "hello.txt"


def test_mv_file_into_directory(session):
    run(session, "mv", "readme.txt", "docs")
    assert "readme.txt" not in names(session)
    assert "readme.txt" in names(session, "docs")


def test_mv_file_to_other_path_with_new_name(session):
    run(session, "mv", "dups.txt", "docs/deep/copy.txt")
    assert "copy.txt" in names(session, "docs/deep")


def test_mv_directory_with_content(session):
    run(session, "mv", "docs", "empty")
    assert names(session, "empty") == ["docs"]
    assert names(session, "empty/docs") == ["deep", "notes.txt"]


def test_mv_overwrites_file(session):
    run(session, "mv", "readme.txt", "dups.txt")
    data = session.vfs.root.children["dups.txt"].data
    assert data.decode("utf-8") == "Привет\nмир\n"
    assert "readme.txt" not in names(session)


def test_mv_no_clobber_keeps_both(session):
    run(session, "mv", "-n", "readme.txt", "dups.txt")
    assert "readme.txt" in names(session)
    data = session.vfs.root.children["dups.txt"].data
    assert data.decode("utf-8").startswith("a\n")


def test_mv_cwd_follows_moved_directory(session):
    run(session, "cd", "docs/deep")
    run(session, "mv", "/docs", "/empty")
    assert run(session, "pwd") == "/empty/docs/deep"
    assert names(session) == ["deeper"]


@pytest.mark.parametrize(
    "arguments",
    [
        [],
        ["readme.txt"],
        ["a", "b", "c"],
        ["-x", "readme.txt", "docs"],
        ["nope", "docs"],
        ["readme.txt", "nope/x"],
        ["readme.txt", "dups.txt/x"],
        ["readme.txt", "readme.txt"],
        ["readme.txt", "/"],
        ["docs", "docs/deep"],
        ["docs", "readme.txt"],
        ["/", "docs"],
    ],
)
def test_mv_errors_leave_vfs_unchanged(session, arguments):
    before = names(session)
    with pytest.raises(CommandError):
        run(session, "mv", *arguments)
    assert names(session) == before