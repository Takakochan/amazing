from mazegen.cell import Cell
from mazegen.cell_value import CellValue
from mazegen.direction import Direction
from mazegen.grid import Grid
from mazegen.render.base import Renderer
from mazegen.solvers.base import Solver


class SolverDFS(Solver):
    def solve(
        self,
        grid: Grid,
        entry: Cell,
        exit: Cell,  # noqa: A002
        renderer: Renderer,
        animation: bool,
    ) -> list[Direction]:
        self._foo = None

        grid.reset_cell_markings()
        grid.unset_parents()

        solution: list[Direction] = []
        stack: list[Cell] = []
        stack.append(entry)

        grid.mark_cell(entry)
        if animation:
            renderer.display_cell(grid, entry)

        while stack:
            current = stack.pop()

            if current == exit:
                break

            for neighbor in grid.get_reachable_unmarked_neighbors(current):
                grid.mark_cell(neighbor)
                grid.set_parent(neighbor, current)

                stack.append(neighbor)

                if animation:
                    renderer.display_cell(grid, neighbor)

        current = exit

        while current is not entry:
            if current != exit:
                grid.set_cell_value(current, CellValue.SOLUTION)

            if animation:
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
