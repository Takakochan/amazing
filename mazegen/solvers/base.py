from abc import ABC, abstractmethod

from mazegen.cell import Cell
from mazegen.grid_animation import GridAnimation


class Solver(ABC):
    @abstractmethod
    def solve(
        self,
        grid: GridAnimation,
        entry: Cell,
        exit: Cell,  # noqa: A002
    ) -> None:
        pass
