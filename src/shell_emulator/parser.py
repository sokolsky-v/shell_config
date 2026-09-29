import os
import shlex


class ParseError(Exception):
    pass


def expand_environment_variables(token: str) -> str:
    return os.path.expandvars(token)


def parse_line(line: str) -> tuple[str, list[str]]:
    stripped_line = line.strip()
    if not stripped_line:
        return "", []

    try:
        raw_tokens = shlex.split(stripped_line, comments=False)
    except ValueError as exc:
        raise ParseError(f"некорректный ввод: {exc}") from exc

    expanded_tokens = [expand_environment_variables(t) for t in raw_tokens]
    command_name, *arguments = expanded_tokens
    return command_name, arguments