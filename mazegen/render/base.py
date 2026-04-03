from abc import ABC, abstractmethod

from mazegen.cell import Cell
from mazegen.direction import Direction
from mazegen.grid import Grid


class Renderer(ABC):
    @abstractmethod
    def write_cell(self, grid: Grid, cell: Cell) -> None:
        pass

    @abstractmethod
    def write_wall(self, grid: Grid, cell: Cell, direction: Direction) -> None:
        pass

    @abstractmethod
    def write_grid(self, grid: Grid) -> None:
        pass

    @abstractmethod
    def flush(self) -> None:
        pass

    def write_cell_with_walls(self, grid: Grid, cell: Cell) -> None:
        self.write_cell(grid, cell)

        for direction in Direction:
            self.write_wall(grid, cell, direction)

    def display_cell(self, grid: Grid, cell: Cell) -> None:
        self.write_cell_with_walls(grid, cell)
        self.flush()

    def display_grid(self, grid: Grid) -> None:
        self.write_grid(grid)
        self.flush()
