from dataclasses import dataclass
from typing import Self

from color import Color
from config import Config


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
    def from_config(cls, config: Config) -> Self:
        return cls(
            config.animation,
            config.animation_speed,
            config.background_color,
            config.wall_color,
            config.entry_color,
            config.exit_color,
            config.forty_two_color,
            config.solution_color,
            config.animation_color,
        )
