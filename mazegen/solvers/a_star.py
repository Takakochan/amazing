import heapq

from mazegen.cell import Cell
from mazegen.cell_value import CellValue
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
    ) -> None:
        self._foo = None

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
                temp = g_score[current.x, current.y] + 1
                g_score[neighbor.x, neighbor.y] = temp

                grid.mark_cell(neighbor)
                grid.set_parent(neighbor, current)

                queue.push(
                    temp + distance(neighbor, exit),
                    neighbor,
                )

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

            current = parent

        grid.reset_cell_markings()
        grid.unset_parents()


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


# TODO: convert to Cell method
def distance(current: Cell, exit: Cell) -> int:  # noqa: A002
    return abs(current.x - exit.x) + abs(current.y - exit.y)
