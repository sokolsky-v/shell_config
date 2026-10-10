"""Модель виртуальной файловой системы. Всё хранится только в памяти."""

from dataclasses import dataclass, field


class VfsError(Exception):
    """Ошибка загрузки или использования VFS."""


@dataclass
class File:
    """Файл VFS: имя и содержимое в байтах."""

    name: str
    data: bytes


@dataclass
class Directory:
    """Каталог VFS: имя и вложенные файлы и каталоги."""

    name: str
    children: dict = field(default_factory=dict)

    def add(self, node):
        """Добавляет узел; повторное имя в одном каталоге недопустимо."""
        if node.name in self.children:
            raise VfsError(f"повторяющееся имя '{node.name}'")
        self.children[node.name] = node


@dataclass
class VfsStats:
    """Сводка по VFS: число каталогов, файлов и глубина вложенности."""

    directories: int
    files: int
    depth: int


def measure(directory):
    """Считает каталоги, файлы и глубину внутри каталога."""
    directories = 0
    files = 0
    depth = 0
    for child in directory.children.values():
        if isinstance(child, Directory):
            inner = measure(child)
            directories += 1 + inner.directories
            files += inner.files
            depth = max(depth, 1 + inner.depth)
        else:
            files += 1
            depth = max(depth, 1)
    return VfsStats(directories, files, depth)


class Vfs:
    """Виртуальная файловая система: имя и корневой каталог."""

    def __init__(self, name, root):
        """Запоминает имя VFS и её корневой каталог."""
        self.name = name
        self.root = root

    def stats(self):
        """Возвращает сводку по всей VFS."""
        return measure(self.root)