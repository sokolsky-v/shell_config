"""Тесты выполнения стартового скрипта."""

from functools import partial

import pytest

from src.shell_emulator.main import handle_line
from src.shell_emulator.script import ScriptError, run_script


def make_script(tmp_path, text):
    path = tmp_path / "script.txt"
    path.write_text(text, encoding="utf-8")
    return str(path)


def test_script_shows_input_and_output(tmp_path, capsys, session):
    path = make_script(tmp_path, "ls a\ncd b\n")
    run_script(path, "vfs> ", partial(handle_line, session))
    out = capsys.readouterr().out
    assert "vfs> ls a" in out
    assert "CMD: ls ARGS: ['a']" in out
    assert "vfs> cd b" in out


def test_script_skips_comments_and_blank_lines(tmp_path, capsys, session):
    path = make_script(tmp_path, "# коммент\n\nls a\n")
    run_script(path, "vfs> ", partial(handle_line, session))
    assert "коммент" not in capsys.readouterr().out


def test_script_stops_on_first_error(tmp_path, capsys, session):
    path = make_script(tmp_path, "ls a\nfoobar\ncd never\n")
    with pytest.raises(ScriptError):
        run_script(path, "vfs> ", partial(handle_line, session))
    assert "never" not in capsys.readouterr().out


def test_missing_script_raises(session):
    with pytest.raises(ScriptError):
        run_script("no_such.txt", "vfs> ", partial(handle_line, session))


def test_exit_in_script_raises_system_exit(tmp_path, session):
    path = make_script(tmp_path, "ls a\nexit\ncd never\n")
    with pytest.raises(SystemExit):
        run_script(path, "vfs> ", partial(handle_line, session))