from mazegen.cell import Cell
from mazegen.grid import Grid
from mazegen.solvers.base import Solver


class SolverAStar(Solver):
    def solve(
        grid: Grid,
        entry: Cell,
        exit: Cell,  # noqa: A002
    ) -> None:
        pass
