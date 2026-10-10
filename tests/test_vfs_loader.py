"""Тесты загрузки VFS из XML."""

import pytest

from src.shell_emulator.vfs import Directory, File, VfsError
from src.shell_emulator.vfs_loader import load_vfs


def write_xml(tmp_path, text, name="v.xml"):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return str(path)


def test_loads_name_and_structure(xml_path):
    vfs = load_vfs(xml_path)
    assert vfs.name == "demo"
    assert isinstance(vfs.root.children["docs"], Directory)
    assert isinstance(vfs.root.children["readme.txt"], File)


def test_text_file_content(xml_path):
    vfs = load_vfs(xml_path)
    data = vfs.root.children["readme.txt"].data
    assert data.decode("utf-8") == "Привет\nмир\n"


def test_base64_file_is_decoded(xml_path):
    vfs = load_vfs(xml_path)
    assert vfs.root.children["data.bin"].data == bytes([0, 1, 2, 3, 4, 255])


def test_stats_of_sample(xml_path):
    stats = load_vfs(xml_path).stats()
    assert (stats.directories, stats.files, stats.depth) == (4, 5, 4)


def test_minimal_vfs_is_empty(tmp_path):
    vfs = load_vfs(write_xml(tmp_path, '<vfs name="m"></vfs>'))
    stats = vfs.stats()
    assert (stats.directories, stats.files, stats.depth) == (0, 0, 0)


def test_name_defaults_to_file_stem(tmp_path):
    vfs = load_vfs(write_xml(tmp_path, "<vfs></vfs>", "mydisk.xml"))
    assert vfs.name == "mydisk"


@pytest.mark.parametrize(
    "text",
    [
        "<vfs><file name='a'>x</vfs>",
        "<other></other>",
        "<vfs><file name='a' encoding='base64'>!!!</file></vfs>",
        "<vfs><file name='a' encoding='base64'>привет</file></vfs>",
        "<vfs><file name='a'/><file name='a'/></vfs>",
        "<vfs><file name='a/b'/></vfs>",
        "<vfs><file/></vfs>",
        "<vfs><link name='a'/></vfs>",
        "<vfs><file name='a' encoding='rot13'>x</file></vfs>",
    ],
)
def test_invalid_vfs_raises(tmp_path, text):
    with pytest.raises(VfsError):
        load_vfs(write_xml(tmp_path, text))


def test_missing_file_raises():
    with pytest.raises(VfsError):
        load_vfs("no_such_vfs.xml")