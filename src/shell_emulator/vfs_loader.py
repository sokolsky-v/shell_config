"""Загрузка VFS из XML-файла прямо в память."""

import base64
import xml.etree.ElementTree as ET
from pathlib import Path

from src.shell_emulator.vfs import Directory, File, Vfs, VfsError

ROOT_TAG = "vfs"
DIR_TAG = "dir"
FILE_TAG = "file"
ENCODING_ATTR = "encoding"
TEXT_ENCODING = "text"
BASE64_ENCODING = "base64"
FORBIDDEN_NAMES = ("", ".", "..")
SEPARATOR = "/"


def _node_name(element):
    """Берёт имя узла из атрибута name и проверяет его допустимость."""
    name = element.get("name")
    if name is None or name in FORBIDDEN_NAMES or SEPARATOR in name:
        raise VfsError(f"недопустимое имя в теге <{element.tag}>: {name!r}")
    return name


def _decode_file(element, name):
    """Возвращает содержимое файла в байтах (текст или base64)."""
    encoding = element.get(ENCODING_ATTR, TEXT_ENCODING)
    text = element.text or ""
    if encoding == TEXT_ENCODING:
        return text.encode("utf-8")
    if encoding == BASE64_ENCODING:
        compact = "".join(text.split())
        try:
            return base64.b64decode(compact, validate=True)
        except ValueError as exc:
            raise VfsError(f"файл '{name}': некорректный base64") from exc
    raise VfsError(f"файл '{name}': неизвестная кодировка '{encoding}'")


def _fill_directory(directory, element):
    """Рекурсивно заполняет каталог по дочерним тегам XML."""
    for child in element:
        name = _node_name(child)
        if child.tag == DIR_TAG:
            sub_directory = Directory(name)
            directory.add(sub_directory)
            _fill_directory(sub_directory, child)
        elif child.tag == FILE_TAG:
            directory.add(File(name, _decode_file(child, name)))
        else:
            raise VfsError(f"неизвестный тег <{child.tag}>")


def load_vfs(path):
    """Читает XML-файл и строит VFS в памяти (файл не изменяется)."""
    try:
        root_element = ET.parse(path).getroot()
    except OSError as exc:
        raise VfsError(f"не удалось открыть '{path}': {exc}") from exc
    except ET.ParseError as exc:
        raise VfsError(f"некорректный XML в '{path}': {exc}") from exc

    if root_element.tag != ROOT_TAG:
        raise VfsError(
            f"корневой тег должен быть <{ROOT_TAG}>, "
            f"а не <{root_element.tag}>"
        )
    name = root_element.get("name") or Path(path).stem
    root = Directory("")
    _fill_directory(root, root_element)
    return Vfs(name, root)