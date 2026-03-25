from abc import ABC, abstractmethod

from mazegen.cell import Cell
from mazegen.grid import Grid


class Solver(ABC):
    @abstractmethod
    def solve(
        grid: Grid,
        entry: Cell,
        exit: Cell,  # noqa: A002
    ) -> None:
        pass
