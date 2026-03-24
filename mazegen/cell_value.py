from enum import Enum, auto


class CellValue(Enum):
    UNMARKED = auto()
    MARKED = auto()

    def __str__(self) -> str:
        match self:
            case CellValue.UNMARKED:
                return " "
            case CellValue.MARKED:
                return "X"
