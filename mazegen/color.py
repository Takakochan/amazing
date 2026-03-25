from enum import Enum, auto

PIXEL = "██"


class Color(Enum):
    NONE = auto()
    BLACK = auto()
    RED = auto()
    GREEN = auto()
    YELLOW = auto()
    BLUE = auto()
    MAGENTA = auto()
    CYAN = auto()
    WHITE = auto()


def print_pixel(color: Color = Color.NONE) -> None:
    match color:
        case Color.NONE:
            print(PIXEL, end="")
        case Color.BLACK:
            print(f"\033[30m{PIXEL}\033[0m", end="")
        case Color.RED:
            print(f"\033[31m{PIXEL}\033[0m", end="")
        case Color.GREEN:
            print(f"\033[32m{PIXEL}\033[0m", end="")
        case Color.YELLOW:
            print(f"\033[33m{PIXEL}\033[0m", end="")
        case Color.BLUE:
            print(f"\033[34m{PIXEL}\033[0m", end="")
        case Color.MAGENTA:
            print(f"\033[35m{PIXEL}\033[0m", end="")
        case Color.CYAN:
            print(f"\033[36m{PIXEL}\033[0m", end="")
        case Color.WHITE:
            print(f"\033[37m{PIXEL}\033[0m", end="")
