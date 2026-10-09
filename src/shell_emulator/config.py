"""Настройки эмулятора: параметры командной строки и XML-конфиг."""

import argparse
import xml.etree.ElementTree as ET
from dataclasses import dataclass


class ConfigError(Exception):
    """Не удалось прочитать конфигурационный файл."""


@dataclass
class Settings:
    """Итоговые настройки запуска эмулятора."""

    vfs_path: str | None = None
    script_path: str | None = None
    config_path: str | None = None


def build_argument_parser():
    """Создаёт разборщик параметров командной строки."""
    parser = argparse.ArgumentParser(
        prog="shell_emulator",
        description="Эмулятор командной строки UNIX-подобной ОС",
    )
    parser.add_argument("--vfs", help="путь к физическому расположению VFS")
    parser.add_argument("--script", help="путь к стартовому скрипту")
    parser.add_argument("--config", help="путь к XML-файлу конфигурации")
    return parser


def parse_arguments(argv=None):
    """Читает параметры командной строки в объект Settings."""
    args = build_argument_parser().parse_args(argv)
    return Settings(
        vfs_path=args.vfs,
        script_path=args.script,
        config_path=args.config,
    )


def _read_text_field(root, tag):
    """Возвращает текст дочернего тега или None, если он пуст/отсутствует."""
    text = root.findtext(tag)
    if text is None or not text.strip():
        return None
    return text.strip()


def read_config_file(path):
    """Читает XML-конфиг, возвращает Settings (только vfs и скрипт)."""
    try:
        root = ET.parse(path).getroot()
    except OSError as exc:
        raise ConfigError(f"не удалось открыть '{path}': {exc}") from exc
    except ET.ParseError as exc:
        raise ConfigError(f"некорректный XML в '{path}': {exc}") from exc

    if root.tag != "config":
        raise ConfigError(
            f"корневой тег должен быть <config>, а не <{root.tag}>"
        )

    return Settings(
        vfs_path=_read_text_field(root, "vfs_path"),
        script_path=_read_text_field(root, "startup_script"),
    )


def merge_settings(from_cli, from_file):
    """Объединяет настройки: значения из CLI главнее значений из файла."""
    return Settings(
        vfs_path=from_cli.vfs_path or from_file.vfs_path,
        script_path=from_cli.script_path or from_file.script_path,
        config_path=from_cli.config_path,
    )


def load_settings(argv=None):
    """Собирает итоговые настройки из CLI и (если указан) XML-конфига."""
    from_cli = parse_arguments(argv)
    if from_cli.config_path is None:
        return from_cli
    from_file = read_config_file(from_cli.config_path)
    return merge_settings(from_cli, from_file)


def format_debug(settings):
    """Строки отладочного вывода всех заданных параметров."""
    def show(value):
        return value if value is not None else "<не задан>"

    return [
        "[debug] Параметры запуска:",
        f"[debug]   vfs    = {show(settings.vfs_path)}",
        f"[debug]   script = {show(settings.script_path)}",
        f"[debug]   config = {show(settings.config_path)}",
    ]