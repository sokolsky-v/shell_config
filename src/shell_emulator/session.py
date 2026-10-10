"""Состояние сеанса работы эмулятора."""

from dataclasses import dataclass, field

from src.shell_emulator.vfs import Vfs


@dataclass
class Session:
    """VFS и текущий каталог (cwd используется с этапа 4)."""

    vfs: Vfs
    cwd: list = field(default_factory=list)