import random

from mazegen.cell import Cell
from mazegen.generators.base import Generator
from mazegen.grid import Grid
from mazegen.render.base import Renderer


class GeneratorDFS(Generator):
    def generate(
        self,
        grid: Grid,
        renderer: Renderer,
        seed: int | None = None,
    ) -> None:
        self._foo = None

        random.seed(seed)

        stack: list[Cell] = []

        edge = [
            cell
            for cell in (
                Cell(x, y)
                for x in range(grid.width)
                for y in range(grid.height)
            )
            if cell.is_at_edge(grid.width, grid.height)
        ]
        cell = random.choice(edge)
        grid.mark_cell(cell)
        stack.append(cell)

        renderer.display_cell(grid, cell)

        while stack:
            current = stack[-1]

            neighbors = grid.get_unmarked_neighbors(current)
            if not neighbors:
                stack.pop()
                continue

            neighbor = random.choice(neighbors)

            try:
                direction = current.get_direction_to_neighbor(neighbor)
            except RuntimeError as error:
                raise error

            grid.open_wall(current, direction)
            grid.mark_cell(neighbor)
            stack.append(neighbor)

            renderer.display_cell(grid, neighbor)

        grid.reset_cell_markings()
