from enum import StrEnum, auto


class Color(StrEnum):
    BLACK = auto()
    RED = auto()
    GREEN = auto()
    YELLOW = auto()
    BLUE = auto()
    MAGENTA = auto()
    CYAN = auto()
    WHITE = auto()

    @staticmethod
    def reset() -> str:
        return "\033[0m"

    def escape_code(self) -> str:
        match self:
            case Color.BLACK:
                return "\033[30m"
            case Color.RED:
                return "\033[31m"
            case Color.GREEN:
                return "\033[32m"
            case Color.YELLOW:
                return "\033[33m"
            case Color.BLUE:
                return "\033[34m"
            case Color.MAGENTA:
                return "\033[35m"
            case Color.CYAN:
                return "\033[36m"
            case Color.WHITE:
                return "\033[37m"
