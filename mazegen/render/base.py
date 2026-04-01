from abc import ABC, abstractmethod

from mazegen.cell import Cell
from mazegen.direction import Direction


class Renderer(ABC):
    @abstractmethod
    def write_cell(self, cell: Cell) -> None:
        pass

    @abstractmethod
    def write_wall(self, cell: Cell, direction: Direction) -> None:
        pass

    @abstractmethod
    def write_cell_with_walls(self, cell: Cell) -> None:
        self.write_cell(cell)

        for direction in Direction:
            self.write_wall(cell, direction)

    @abstractmethod
    def write_grid(self) -> None:
        pass

    @abstractmethod
    def flush(self) -> None:
        pass
