from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Any, Self

from numpy.char import isnumeric
from returns.result import Failure, Result, Success

if TYPE_CHECKING:
    from collections.abc import Callable


def parse_int(value: str) -> Result[int, Exception]:
    if isnumeric(value):
        return Success(int(value))

    return Failure(f"invalid integer: `{value}`")


def parse_int_tuple(value: str) -> Result[tuple[int, int], Exception]:
    split_value = value.split(",", 1)

    if len(split_value) != 2:
        return Failure(f"invalid tuple: `{value}`")

    return Result.do((x, y) for x in split_value[0] for y in split_value[1])


def parse_bool(value: str) -> Result[bool, Exception]:
    if value == "True":
        return Success(True)

    if value == "False":
        return Success(False)

    return Failure(f"invalid literal for boolean: `{value}`")


def parse_str(value: str) -> Result[str, Exception]:
    return Success(value)


def parse_line(config: dict[str, Any], line: str) -> Result[None, Exception]:
    stripped_line = line.strip()

    if not stripped_line or stripped_line.startswith("#"):
        return Success(None)

    split_line = stripped_line.split("=", 1)

    if len(split_line) != 2:
        return Failure(f"missing `=` in line: `{stripped_line}`")

    key = split_line[0]
    value = split_line[1]

    if key not in [field.name.upper() for field in fields(Config)]:
        return Failure(f"invalid key: '{key}'")

    parser: Callable[[str], Result[Any, Exception]] = (
        Config.__dataclass_fields__[key.lower()].metadata["parser"]
    )

    match parser(value):
        case Success(result):
            config[key.lower()] = result
        case Failure(error):
            return Failure(error)

    return Success(None)


@dataclass
class Config:
    width: int = field(metadata={"parser": parse_int})
    height: int = field(metadata={"parser": parse_int})
    entry: tuple[int, int] = field(metadata={"parser": parse_int_tuple})
    exit: tuple[int, int] = field(metadata={"parser": parse_int_tuple})
    output_file: str = field(metadata={"parser": parse_str})
    perfect: bool = field(metadata={"parser": parse_bool})

    @classmethod
    def from_file(cls, filename: str) -> Result[Self, None]:
        try:
            with open(filename, encoding="utf-8") as file:
                config: dict[str, Any] = {}

                for line in file:
                    match parse_line(config, line):
                        case Success(None):
                            pass
                        case Failure(err):
                            return Failure(err)

                try:
                    return Success(cls(**config))
                except Exception as err:
                    return Failure(f"missing key/value pair: {err}")
        except OSError as error:
            return Failure(error)


if __name__ == "__main__":
    match Config.from_file("config.txt"):
        case Success(config):
            print(f"config: {config}")
        case Failure(error):
            print(f"Error: {error}")
