from abc import ABC, abstractmethod

from mazegen.animation import GridDisplayer
from mazegen.cell import Cell


class Solver(ABC):
    @abstractmethod
    def solve(
        self,
        grid: GridDisplayer,
        entry: Cell,
        exit: Cell,  # noqa: A002
    ) -> None:
        pass
