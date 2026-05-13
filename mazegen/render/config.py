import random
from dataclasses import dataclass
from typing import Self

from mazegen.color import Color


@dataclass
class RenderConfig:
    animation: bool
    animation_speed: int
    background_color: Color
    wall_color: Color
    entry_color: Color
    exit_color: Color
    forty_two_color: Color
    solution_color: Color
    animation_color: Color

    @classmethod
    def default(cls) -> Self:
        return cls(
            False,
            100,
            Color.BLACK,
            Color.WHITE,
            Color.GREEN,
            Color.RED,
            Color.YELLOW,
            Color.MAGENTA,
            Color.BLUE,
        )

    def randomize(self) -> None:
        (
            self.background_color,
            self.wall_color,
            self.entry_color,
            self.exit_color,
            self.forty_two_color,
            self.solution_color,
            self.animation_color,
        ) = random.sample(list(Color), 7)
