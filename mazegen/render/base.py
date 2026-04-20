from abc import ABC, abstractmethod

from mazegen.cell import Cell
from mazegen.direction import Direction
from mazegen.grid import Grid


class Renderer(ABC):
    @abstractmethod
    def animate(self) -> bool:
        pass

    @abstractmethod
    def show_solution(self) -> bool:
        pass

    @abstractmethod
    def hide_solution(self) -> bool:
        pass

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
    def display_cell(self, grid: Grid, cell: Cell) -> None:
        pass

    @abstractmethod
    def display_grid(self, grid: Grid) -> None:
        pass

    @abstractmethod
    def random_color(self, grid: Grid) -> None:
        pass
