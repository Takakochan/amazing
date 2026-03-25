from enum import Enum
from typing import Self

from mazegen.color import Color


class CellValue(Enum):
    NONE = 99
    ENTRY = 1
    EXIT = 2
    FORTY_TWO = 3
    SOLUTION = 4

    def into_color(self) -> Color:
        match self:
            case CellValue.NONE:
                return Color.BLACK
            case CellValue.ENTRY:
                return Color.GREEN
            case CellValue.EXIT:
                return Color.RED
            case CellValue.FORTY_TWO:
                return Color.YELLOW
            case CellValue.SOLUTION:
                return Color.MAGENTA

    def __gt__(self, other: Self) -> bool:
        return self.value > other.value

    def __ge__(self, other: Self) -> bool:
        return self.value >= other.value

    def __lt__(self, other: Self) -> bool:
        return self.value < other.value

    def __le__(self, other: Self) -> bool:
        return self.value <= other.value
