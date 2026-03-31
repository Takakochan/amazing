from mazegen.animation import GridDisplayer
from mazegen.cell import Cell
from mazegen.cell_value import CellValue
from mazegen.solvers.base import Solver


class SolverBFS(Solver):
    def solve(
        self,
        grid: GridDisplayer,
        entry: Cell,
        exit: Cell,  # noqa: A002
    ) -> None:
        self._foo = None

        grid.reset_cell_markings()
        grid.unset_parents()

        queue: list[Cell] = []

        grid.mark_cell(entry)
        queue.append(entry)

        grid.display_cell(entry)

        while queue:
            current = queue.pop(0)
            if current == exit:
                break

            for neighbor in grid.get_reachable_unmarked_neighbors(current):
                grid.mark_cell(neighbor)
                grid.set_parent(neighbor, current)
                queue.append(neighbor)

                grid.display_cell(neighbor)

        current = exit

        while current is not entry:
            if current != exit:
                grid.set_cell_value(current, CellValue.SOLUTION)

            grid.display_cell(current)

            parent = grid.get_parent(current)
            if parent is None:
                break

            current = parent

        grid.reset_cell_markings()
        grid.unset_parents()
