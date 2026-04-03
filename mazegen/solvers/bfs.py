from mazegen.cell import Cell
from mazegen.cell_value import CellValue
from mazegen.direction import Direction
from mazegen.grid import Grid
from mazegen.render.base import Renderer
from mazegen.solvers.base import Solver


class SolverBFS(Solver):
    def solve(
        self,
        grid: Grid,
        entry: Cell,
        exit: Cell,  # noqa: A002
        renderer: Renderer,
    ) -> list[Direction]:
        self._foo = None

        grid.reset_cell_markings()
        grid.unset_parents()

        solution: list[Direction] = []
        queue: list[Cell] = []
        queue.append(entry)

        grid.mark_cell(entry)
        renderer.display_cell(grid, entry)

        while queue:
            current = queue.pop(0)
            if current == exit:
                break

            for neighbor in grid.get_reachable_unmarked_neighbors(current):
                grid.mark_cell(neighbor)
                grid.set_parent(neighbor, current)

                queue.append(neighbor)

                renderer.display_cell(grid, neighbor)

        current = exit

        while current is not entry:
            if current != exit:
                grid.set_cell_value(current, CellValue.SOLUTION)

            renderer.display_cell(grid, current)

            parent = grid.get_parent(current)
            if parent is None:
                break

            direction = parent.get_direction_to_neighbor(current)
            solution.insert(0, direction)

            current = parent

        grid.reset_cell_markings()
        grid.unset_parents()

        return solution
