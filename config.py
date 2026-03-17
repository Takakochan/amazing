from collections.abc import Callable
from dataclasses import dataclass, fields
from typing import Any, Self, get_type_hints

type ParserFn = Callable[[str], Any]

PARSERS: dict[str, ParserFn] = {}


class ConfigError(Exception):
    pass


def register_parser(fn: ParserFn) -> ParserFn:
    return_type = get_type_hints(fn).get("return")

    if return_type is None:
        raise ConfigError(f"parser function `{fn}` returns `None`")

    if PARSERS.get(return_type) is not None:
        raise ConfigError(
            f"parser function already defined for `{return_type}`",
        )

    PARSERS[return_type] = fn

    return fn


@register_parser
def parse_int(value: str) -> int:
    try:
        return int(value)
    except ValueError as error:
        raise ConfigError(f"invalid integer: `{value}`") from error


@register_parser
def parse_int_tuple(value: str) -> tuple[int, int]:
    split_value = value.split(",", 1)

    if len(split_value) != 2:
        raise ConfigError("expected two values seperated by a comma")

    try:
        x = parse_int(split_value[0])
    except ConfigError as error:
        raise error

    try:
        y = parse_int(split_value[1])
    except ConfigError as error:
        raise error

    return (x, y)


@register_parser
def parse_bool(value: str) -> bool:
    if value == "True":
        return True

    if value == "False":
        return False

    raise ConfigError(f"invalid boolean literal: `{value}`")


@register_parser
def parse_str(value: str) -> str:
    return value


def parse_line(config: dict[str, Any], line: str) -> None:
    stripped_line = line.strip()

    if not stripped_line or stripped_line.startswith("#"):
        return

    split_line = stripped_line.split("=", 1)

    if len(split_line) != 2:
        raise ConfigError("expected two values seperated by =")

    key = split_line[0]
    value = split_line[1]

    field_names: list[str] = [field.name.upper() for field in fields(Config)]
    field_types: list[Any] = [field.type for field in fields(Config)]

    try:
        index = field_names.index(key)
    except ValueError as error:
        raise ConfigError(f"invalid key: `{key}`") from error

    field_type = field_types[index]
    parser = PARSERS[field_type]

    try:
        result = parser(value)
    except ConfigError as error:
        raise error

    config[key.lower()] = result


@dataclass
class Config:
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool

    @classmethod
    def from_file(cls, filepath: str) -> Self | None:
        try:
            with open(filepath, encoding="utf-8") as file:
                config: dict[str, Any] = {}

                for line in file:
                    parse_line(config, line)

                try:
                    return cls(**config)
                except KeyError as error:
                    raise ConfigError("missing key/value pair") from error
        except OSError as error:
            raise ConfigError(f"failed to open file: `{filepath}`") from error


if __name__ == "__main__":
    try:
        config = Config.from_file("config.txt")
        print(f"config: {config}")
    except ConfigError as err:
        print(f"ERROR: {err}")
