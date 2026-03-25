from abc import ABC, abstractmethod

from mazegen.grid import Grid


class Solver(ABC):
    @abstractmethod
    def solve(grid: Grid) -> None:
        pass
