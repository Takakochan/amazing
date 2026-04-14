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
        src: Cell,
        dest: Cell,
        renderer: Renderer,
    ) -> list[Direction]:
        self._foo = None

        grid.reset_cell_markings()
        grid.unset_parents()

        solution: list[Direction] = []
        queue = PriorityQueue(dest)
        queue.push(src, None)

        grid.mark_cell(src)
        if renderer.animate():
            renderer.display_cell(grid, src)

        while not queue.is_empty():
            current = queue.pop()
            if current is None:
                break
            if current == dest:
                break

            for neighbor in grid.get_reachable_unmarked_neighbors(current):
                queue.push(neighbor, current)

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


class PriorityQueue:
    def __init__(self, dest: Cell) -> None:
        self._heap: list[tuple[int, int, Cell]] = []
        self._distance: dict[Cell, int] = {}
        self._counter: int = 0
        self._dest = dest

    def push(self, cell: Cell, parent: Cell | None) -> None:
        assert self._distance.get(cell) is None, (
            f"already visited cell `{cell}`"
        )

        distance = 0
        if parent is not None:
            distance_parent = self._distance.get(parent)
            assert distance_parent is not None, (
                f"not yet visited parent cell `{parent}`"
            )
            distance = distance_parent + 1

        self._distance[cell] = distance

        priority = self._distance[cell] + cell.distance_to(self._dest)
        heapq.heappush(self._heap, (priority, self._counter, cell))
        self._counter += 1

    def pop(self) -> Cell | None:
        if not self._heap:
            return None

        _priority, _counter, cell = heapq.heappop(self._heap)

        return cell

    def is_empty(self) -> bool:
        return len(self._heap) == 0
