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

    def save(self) -> None:
        with open(self.config.output_file, "w", encoding="utf-8") as file:
            for cell_list in self.grid.get_cell_state_grid():
                for cell in cell_list:
                    file.write(cell.to_hex())
                file.write("\n")
            file.write("\n")

            file.write(f"{self.config.entry[0]},{self.config.entry[1]}\n")
            file.write(f"{self.config.exit[0]},{self.config.exit[1]}\n")

            # TODO: write solution to output file
            file.write("<solution>\n")
