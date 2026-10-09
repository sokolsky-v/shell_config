"""Тесты чтения параметров CLI и XML-конфига."""

import pytest

from src.shell_emulator.config import (
    ConfigError,
    Settings,
    format_debug,
    load_settings,
    merge_settings,
    read_config_file,
)


def write_config(tmp_path, text):
    path = tmp_path / "config.xml"
    path.write_text(text, encoding="utf-8")
    return str(path)


def test_cli_only():
    settings = load_settings(["--vfs", "a.xml", "--script", "s.txt"])
    assert settings.vfs_path == "a.xml"
    assert settings.script_path == "s.txt"
    assert settings.config_path is None


def test_read_config_file(tmp_path):
    path = write_config(
        tmp_path,
        "<config><vfs_path>v.xml</vfs_path>"
        "<startup_script>s.txt</startup_script></config>",
    )
    settings = read_config_file(path)
    assert settings.vfs_path == "v.xml"
    assert settings.script_path == "s.txt"


def test_cli_has_priority_over_config(tmp_path):
    path = write_config(
        tmp_path,
        "<config><vfs_path>file.xml</vfs_path>"
        "<startup_script>file.txt</startup_script></config>",
    )
    settings = load_settings(["--config", path, "--vfs", "cli.xml"])
    assert settings.vfs_path == "cli.xml"
    assert settings.script_path == "file.txt"


def test_missing_config_file_raises():
    with pytest.raises(ConfigError):
        read_config_file("no_such_file.xml")


def test_broken_xml_raises(tmp_path):
    path = write_config(tmp_path, "<config><vfs_path>x</config>")
    with pytest.raises(ConfigError):
        read_config_file(path)


def test_wrong_root_tag_raises(tmp_path):
    path = write_config(tmp_path, "<settings></settings>")
    with pytest.raises(ConfigError):
        read_config_file(path)


def test_merge_keeps_file_value_when_cli_empty():
    merged = merge_settings(Settings(), Settings(vfs_path="f.xml"))
    assert merged.vfs_path == "f.xml"


def test_debug_output_lists_all_parameters():
    lines = format_debug(Settings(vfs_path="a.xml"))
    text = "\n".join(lines)
    assert "a.xml" in text
    assert "<не задан>" in text