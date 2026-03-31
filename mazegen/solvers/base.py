from abc import ABC, abstractmethod

from mazegen.cell import Cell
from mazegen.grid import Grid


class Solver(ABC):
    @abstractmethod
    def solve(grid: Grid, entry: Cell, exit: Cell) -> None:  # noqa: A002
        pass
