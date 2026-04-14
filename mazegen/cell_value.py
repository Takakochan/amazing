from enum import IntEnum

from color import Color
from mazegen.render.config import RenderConfig


class CellValue(IntEnum):
    NONE = 99
    ENTRY = 1
    EXIT = 2
    FORTY_TWO = 3
    SOLUTION = 4

    def into_color(self, config: RenderConfig) -> Color:
        match self:
            case CellValue.NONE:
                return config.background_color
            case CellValue.ENTRY:
                return config.entry_color
            case CellValue.EXIT:
                return config.exit_color
            case CellValue.FORTY_TWO:
                return config.forty_two_color
            case CellValue.SOLUTION:
                return config.solution_color
