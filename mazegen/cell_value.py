from enum import Enum, auto

from mazegen.color import Color


class CellValue(Enum):
    UNMARKED = auto()
    MARKED = auto()
    ENTRY = auto()
    EXIT = auto()
    FORTY_TWO = auto()
    GEN_START = auto()

    def into_color(self) -> Color:
        match self:
            case CellValue.UNMARKED:
                return Color.BLACK
            case CellValue.MARKED:
                return Color.BLUE
            case CellValue.ENTRY:
                return Color.GREEN
            case CellValue.EXIT:
                return Color.RED
            case CellValue.FORTY_TWO:
                return Color.YELLOW
            case CellValue.GEN_START:
                return Color.MAGENTA
