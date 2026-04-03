from abc import ABC, abstractmethod

from mazegen.cell import Cell
from mazegen.direction import Direction
from mazegen.grid import Grid
from mazegen.render.base import Renderer


class Solver(ABC):
    @abstractmethod
    def solve(
        self,
        grid: Grid,
        entry: Cell,
        exit: Cell,  # noqa: A002
        renderer: Renderer,
    ) -> list[Direction]:
        pass
