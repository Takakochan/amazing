from abc import ABC, abstractmethod

from src.mazegen.cell import Cell
from src.mazegen.direction import Direction
from src.mazegen.grid import Grid
from src.mazegen.render.base import Renderer


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
