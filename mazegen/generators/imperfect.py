import random
import time

from mazegen.cell import Cell
from mazegen.generators.base import Generator
from mazegen.generators.dfs import GeneratorDFS
from mazegen.grid import Grid
from mazegen.render.base import Renderer


class GeneratorImperfect(Generator):
    def generate(
        self,
        grid: Grid,
        seed: int | None,
        renderer: Renderer,
    ) -> int:
        if seed is None:
            seed = time.time_ns()
        generator = GeneratorDFS()
        generator.generate(grid, seed, renderer)
        closed_walls = grid.get_collect_closed_walls()
        self._open_random_walls(grid, renderer, closed_walls)
        with open('/tmp/closed_walls.txt', 'w') as f:
            for cell, direction in closed_walls:
                f.write(f"Cell({cell.x}, {cell.y}) - {direction.name}\n")
        return seed

    @staticmethod
    def _open_random_walls(
        grid: Grid,
        renderer: Renderer,
        closed_walls: list[tuple[Cell, Direction]],
        ratio: float = 0.2,
    ) -> None:
        count = max(1, int(len(closed_walls) * ratio))
        chosen = random.sample(closed_walls, min(count, len(closed_walls)))
        for cell, direction in chosen:
            grid.open_wall(cell, direction)
            if renderer.animate():
                renderer.display_cell(grid, cell)

    # @staticmethod
    # def _open_walls_by_areas(
    #     grid: Grid,
    #     renderer: Renderer,
    #     closed_walls: list,
    # ) -> None:
        
    #     area_a = [Cell(x, y) for x, y in 