import heapq

from mazegen.cell import Cell
from mazegen.cell_value import CellValue
from mazegen.direction import Direction
from mazegen.grid import Grid
from mazegen.render.base import Renderer
from mazegen.solvers.base import Solver


class SolverAStar(Solver):
    def solve(
        self,
        grid: Grid,
        entry: Cell,
        exit: Cell,  # noqa: A002
        renderer: Renderer,
    ) -> list[Direction]:
        self._foo = None

        solution: list[Direction] = []

        queue = PriorityQueue()
        queue.push(0, entry)
        g_score = {(entry.x, entry.y): 0}

        while not queue.is_empty():
            current = queue.pop()
            if current is None:
                break
            if current == exit:
                break

            for neighbor in grid.get_reachable_unmarked_neighbors(current):
                score = g_score[current.x, current.y] + 1
                g_score[neighbor.x, neighbor.y] = score

                grid.mark_cell(neighbor)
                grid.set_parent(neighbor, current)

                queue.push(score + neighbor.distance_to(exit), neighbor)

                renderer.display_cell(grid, neighbor)

        renderer.display_grid(grid)

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


class PriorityQueue:
    def __init__(self) -> None:
        self._heap: list[tuple[int, int, Cell]] = []
        self._counter: int = 0

    def push(self, priority: int, cell: Cell) -> None:
        heapq.heappush(self._heap, (priority, self._counter, cell))
        self._counter += 1

    def pop(self) -> Cell | None:
        if not self._heap:
            return None

        _priority, _counter, cell = heapq.heappop(self._heap)

        return cell

    def is_empty(self) -> bool:
        return len(self._heap) == 0
