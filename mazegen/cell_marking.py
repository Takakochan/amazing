from enum import Enum, auto

from color import Color
from mazegen.render.config import RenderConfig


class CellMarking(Enum):
    UNMARKED = auto()
    MARKED = auto()

    def into_color(self, config: RenderConfig) -> Color:
        match self:
            case CellMarking.UNMARKED:
                return config.background_color
            case CellMarking.MARKED:
                return config.animation_color
