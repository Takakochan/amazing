from mazegen.cell import Cell
from mazegen.cell_value import CellValue
from mazegen.grid import Grid
from mazegen.solvers.base import Solver


class SolverBFS(Solver):
    def solve(
        self,
        grid: Grid,
        entry: Cell,
        exit: Cell,  # noqa: A002
    ) -> None:
        grid.reset_cell_markings()
        grid.unset_parents()

        queue: list[Cell] = []

        grid.mark_cell(entry)
        queue.append(entry)

        while queue:
            current = queue.pop(0)
            if current == exit:
                break

            for neighbor in grid.get_reachable_unmarked_neighbors(current):
                grid.mark_cell(neighbor)
                grid.set_parent(neighbor, current)
                queue.append(neighbor)

            grid.display()

        current = exit

        while current is not entry:
            if current != exit:
                grid.set_cell_value(current, CellValue.SOLUTION)

            parent = grid.get_parent(current)
            if parent is None:
                break

            current = parent

            grid.display()

        grid.reset_cell_markings()
        grid.unset_parents()
