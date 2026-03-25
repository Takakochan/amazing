from enum import Enum, auto

from mazegen.color import Color


class CellMarking(Enum):
    UNMARKED = auto()
    MARKED = auto()

    def into_color(self) -> Color:
        match self:
            case CellMarking.UNMARKED:
                return Color.BLACK
            case CellMarking.MARKED:
                return Color.BLUE
