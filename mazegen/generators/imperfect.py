import random
import time

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
        self._open_walls_by_areas(grid, renderer, closed_walls)
        with open('/tmp/closed_walls.txt', 'w') as f:
            for cell, direction in closed_walls:
                f.write(f"Cell({cell.x}, {cell.y}) - {direction.name}\n")
        return seed

    @staticmethod
    def _open_random_walls(
        grid: Grid,
        renderer: Renderer,
        closed_walls: list,
        ratio: float = 0.2,
    ) -> None:
        count = max(1, int(len(closed_walls) * ratio))
        chosen = random.sample(closed_walls, min(count, len(closed_walls)))
        for cell, direction in chosen:
            grid.open_wall(cell, direction)
            if renderer.animate():
                renderer.display_cell(grid, cell)

    @staticmethod
    def _open_walls_by_areas(
        grid: Grid,
        renderer: Renderer,
        closed_walls: list,
    ) -> None:
        mid_x = grid.width // 2
        mid_y = grid.height // 2
        area_a = [(cell, direction) for cell, direction in closed_walls
                  if 0 < cell.x <= mid_x and 0 < cell.y <= mid_y]
        area_b = [(cell, direction) for cell, direction in closed_walls
                  if mid_x < cell.x < grid.width
                  and mid_y < cell.y < grid.height]
        area_c = [(cell, direction) for cell, direction in closed_walls
                  if 0 < cell.x <= mid_x and mid_y < cell.y < grid.height]
        area_d = [(cell, direction) for cell, direction in closed_walls
                  if mid_x < cell.x < grid.width and 0 < cell.y <= mid_y]
        areas = [area_a, area_b, area_c, area_d]
        for a in areas:
            if not a:
                continue
            cell, direction = random.choice(a)
            grid.open_wall(cell, direction)
            if renderer.animate():
                renderer.display_cell(grid, cell)