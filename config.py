from collections.abc import Callable
from dataclasses import dataclass, fields
from typing import Any, Literal, Self, get_args, get_type_hints

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


@register_parser
def parse_algorithm(value: str) -> Literal["BFS", "A*"]:
    match value:
        case "BFS":
            return "BFS"
        case "A*":
            return "A*"
        case _:
            raise ConfigError(f"invalid algorithm: `{value}`")


def get_parser(key: str) -> ParserFn:
    field_names: list[str] = [field.name.upper() for field in fields(Config)]
    field_types: list[Any] = [field.type for field in fields(Config)]

    try:
        index = field_names.index(key)
    except ValueError as error:
        raise ConfigError(f"invalid key: `{key}`") from error

    field_type = field_types[index]
    type_args = get_args(field_type)

    if len(type_args) <= 1 or type_args[-1] is not type(None):
        return PARSERS[field_type]

    parts = tuple(arg for arg in type_args)

    if len(parts) == 1:
        return PARSERS[parts[0]]

    union = parts[0]

    for part in parts[1:-1]:
        union |= part

    return PARSERS[union]


def parse_line(config: dict[str, Any], line: str) -> None:
    stripped_line = line.strip()

    if not stripped_line or stripped_line.startswith("#"):
        return

    split_line = stripped_line.split("=", 1)

    if len(split_line) != 2:
        raise ConfigError("expected two values seperated by =")

    key = split_line[0]
    value = split_line[1]

    try:
        parser = get_parser(key)
    except ConfigError as error:
        raise error

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
    algorithm: Literal["BFS", "A*"] | None = None
    seed: int | None = None

    @classmethod
    def from_file(cls, filepath: str) -> Self:
        try:
            with open(filepath, encoding="utf-8") as file:
                config: dict[str, Any] = {}

                for line in file:
                    parse_line(config, line)

                try:
                    cfg = cls(**config)
                except KeyError as error:
                    raise ConfigError("missing key/value pair") from error

                try:
                    cfg.validate()
                except ConfigError as error:
                    raise error

                return cfg
        except OSError as error:
            raise ConfigError(f"failed to open file: `{filepath}`") from error

    def validate(self) -> None:
        if self.width <= 0:
            raise ConfigError(f"width must be positive: `{self.width}`")

        if self.height <= 0:
            raise ConfigError(f"height must be positive: `{self.height}`")

        if (
            self.entry[0] < 0
            or self.entry[0] >= self.width
            or self.entry[1] < 0
            or self.entry[1] >= self.height
        ):
            raise ConfigError(f"entry must be in grid range: `{self.entry}`")

        if (
            self.exit[0] < 0
            or self.exit[0] >= self.width
            or self.exit[1] < 0
            or self.exit[1] >= self.height
        ):
            raise ConfigError(f"exit must be in grid range: `{self.exit}`")
