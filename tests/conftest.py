"""Общие данные для тестов: пример VFS и сеанс с ней."""

import pytest

from src.shell_emulator.session import Session
from src.shell_emulator.vfs_loader import load_vfs

SAMPLE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<vfs name="demo">
<file name="readme.txt">Привет
мир
</file>
<file name="dups.txt">a
a
b
b
b
c
a
</file>
<file name="data.bin" encoding="base64">AAECAwT/</file>
<dir name="docs">
<file name="notes.txt">1
2
3
4
5
6
7
8
9
10
11
12
</file>
<dir name="deep">
<dir name="deeper">
<file name="file.txt">глубоко
</file>
</dir>
</dir>
</dir>
<dir name="empty"/>
</vfs>
"""


@pytest.fixture
def xml_path(tmp_path):
    """Путь к XML-файлу с примером VFS."""
    path = tmp_path / "demo.xml"
    path.write_text(SAMPLE_XML, encoding="utf-8")
    return str(path)


@pytest.fixture
def session(xml_path):
    """Сеанс, в котором загружена пример VFS."""
    return Session(load_vfs(xml_path))