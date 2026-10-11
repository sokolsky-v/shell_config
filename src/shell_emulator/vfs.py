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
    

def normalize(cwd, path):
    """Превращает путь (абсолютный или относительный) в список имён.

    Понимает '.', '..' и повторные '/'. Выше корня подняться нельзя.
    """
    parts = [] if path.startswith("/") else list(cwd)
    for part in path.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if parts:
                parts.pop()
        else:
            parts.append(part)
    return parts


def lookup(vfs, parts):
    """Находит узел VFS по списку имён от корня."""
    node = vfs.root
    for part in parts:
        if not isinstance(node, Directory):
            raise VfsError("не является каталогом")
        if part not in node.children:
            raise VfsError("нет такого файла или каталога")
        node = node.children[part]
    return node


def _labeled(label, text):
    """Добавляет к тексту ошибки пояснение, если оно задано."""
    return f"{label}: {text}" if label else text


def _lookup_labeled(vfs, parts, label):
    """Как lookup, но добавляет к тексту ошибки пояснение (label)."""
    try:
        return lookup(vfs, parts)
    except VfsError as exc:
        raise VfsError(_labeled(label, str(exc))) from exc


def _parent_and_name(vfs, parts, label=None):
    """Возвращает (каталог-родитель, имя) для непустого пути."""
    parent = _lookup_labeled(vfs, parts[:-1], label)
    if not isinstance(parent, Directory):
        raise VfsError(_labeled(label, "не является каталогом"))
    return parent, parts[-1]


def create_file(vfs, parts):
    """Создаёт пустой файл. Существующий узел не меняется.

    Возвращает True, если файл был создан.
    """
    if not parts:
        return False
    parent, name = _parent_and_name(vfs, parts)
    if name in parent.children:
        return False
    parent.add(File(name, b""))
    return True


def _final_destination(vfs, src, dst):
    """Если назначение - существующий каталог, перемещаем внутрь него."""
    try:
        target = lookup(vfs, dst)
    except VfsError:
        return dst
    if isinstance(target, Directory):
        return dst + [src[-1]]
    return dst


def _check_replaceable(node, existing):
    """Заменить можно только файл файлом."""
    if isinstance(node, Directory) or isinstance(existing, Directory):
        raise VfsError("назначение уже существует")


def move_node(vfs, src, dst, overwrite=True):
    """Перемещает или переименовывает узел внутри VFS.

    Возвращает итоговый путь (список имён) или None, если перемещение
    пропущено из-за запрета перезаписи (overwrite=False).
    """
    node = _lookup_labeled(vfs, src, "источник")
    if not src:
        raise VfsError("нельзя переместить корневой каталог")
    dst = _final_destination(vfs, src, dst)
    if dst == src:
        raise VfsError("источник и назначение совпадают")
    if dst[: len(src)] == src:
        raise VfsError("нельзя переместить каталог в самого себя")
    parent, name = _parent_and_name(vfs, dst, "назначение")
    existing = parent.children.get(name)
    if existing is not None:
        if not overwrite:
            return None
        _check_replaceable(node, existing)
    old_parent = lookup(vfs, src[:-1])
    del old_parent.children[src[-1]]
    node.name = name
    parent.children[name] = node
    return dst