from dataclasses import dataclass
from typing import Self

from config import Config, ConfigError
from grid import Grid


@dataclass
class Maze:
    config: Config
    grid: Grid

    @classmethod
    def from_config_file(cls, filepath: str) -> Self:
        try:
            config = Config.from_file(filepath)
            grid = Grid(config.width, config.height)
            return cls(config, grid)
        except ConfigError as error:
            raise error

    def display(self) -> None:
        print(f"{self.config}")
        self.grid.display()
