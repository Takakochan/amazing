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
        src: Cell,
        dest: Cell,
        renderer: Renderer,
    ) -> list[Direction]:
        pass
