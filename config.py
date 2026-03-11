from collections.abc import Callable
from dataclasses import dataclass, fields
from typing import Any, Self, get_type_hints

# TODO: convert to fallible function
type ParserFn[T] = Callable[[str], T]

PARSERS: dict[str, ParserFn] = {}


def register_parser(fn: ParserFn) -> ParserFn:
    return_type = get_type_hints(fn).get("return")

    # TODO: error if return_type is None
    # TODO: error if PARSERS[return_type] is already defined

    if return_type is not None:
        PARSERS[return_type.__name__] = fn

    return fn


@register_parser
def parse_int(value: str) -> int:
    return int(value)


@register_parser
def parse_int_tuple(value: str) -> tuple[int, int]:
    split_value = value.split(",", 1)
    x = parse_int(split_value[0])
    y = parse_int(split_value[1])
    return (x, y)


@register_parser
def parse_bool(value: str) -> bool:
    if value == "True":
        return True

    if value == "False":
        return False

    raise ValueError(f"invalid literal for boolean: '{value}'")


@register_parser
def parse_str(value: str) -> str:
    return value


# TODO: convert to fallible function


def parse_line(config: dict, line: str) -> None:
    stripped_line = line.strip()

    if not stripped_line or stripped_line.startswith("#"):
        return

    split_line = stripped_line.split("=", 1)

    # TODO: verify there are 2 items in split_line

    key = split_line[0]
    value = split_line[1]

    field_names: list[str] = [field.name.upper() for field in fields(Config)]
    field_types: list[Any] = [field.type for field in fields(Config)]

    try:
        index = field_names.index(key)
    except ValueError as err:
        raise ValueError(f"invalid key: '{key}'") from err

    field_type = field_types[index]
    parser = PARSERS[field_type.__name__]
    result = parser(value)

    # TODO: handle parser error

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
    def from_file(cls, filename: str) -> Self | None:
        try:
            with open(filename, encoding="utf-8") as file:
                config = {}

                for line in file:
                    parse_line(config, line)

                try:
                    return cls(**config)
                except Exception as err:
                    print(f"missing key/value pair: {err}")
        except OSError as error:
            print(f"{error}")


if __name__ == "__main__":
    try:
        config = Config.from_file("config.txt")
        print(f"config: {config}")
    except Exception as err:
        print(f"Exception: {err}")
