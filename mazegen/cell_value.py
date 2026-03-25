from enum import Enum, auto


class CellValue(Enum):
    UNMARKED = auto()
    MARKED = auto()
    ENTRY = auto()
    EXIT = auto()
    FORTY_TWO = auto()
