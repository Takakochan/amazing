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
        src: Cell,
        dest: Cell,
        renderer: Renderer,
    ) -> list[Direction]:
        self._foo = None

        grid.reset_cell_markings()
        grid.unset_parents()

        solution: list[Direction] = []
        queue: list[Cell] = []
        queue.append(src)

        grid.mark_cell(src)
        if renderer.animate():
            renderer.display_cell(grid, src)

        while queue:
            current = queue.pop(0)
            if current == dest:
                break

            for neighbor in grid.get_reachable_unmarked_neighbors(current):
                queue.append(neighbor)

                grid.set_parent(neighbor, current)
                grid.mark_cell(neighbor)
                if renderer.animate():
                    renderer.display_cell(grid, neighbor)

        current = dest

        while current is not src:
            if current != dest:
                grid.set_cell_value(current, CellValue.SOLUTION)

            if renderer.animate():
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
