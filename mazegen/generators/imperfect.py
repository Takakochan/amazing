import random
import time

from mazegen.cell import Cell
from mazegen.direction import Direction
from mazegen.generators.base import Generator
from mazegen.generators.dfs import GeneratorDFS
from mazegen.grid import Grid
from mazegen.render.base import Renderer
from mazegen.wall_state import WallState


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

    @staticmethod
    def _open_walls_by_areas(
        grid: Grid,
        renderer: Renderer,
        closed_walls: list[tuple[Cell, Direction]],
    ) -> None:
        mid_x = grid.width // 2
        mid_y = grid.height // 2
        area_a = [
            (cell, direction)
            for cell, direction in closed_walls
            if 0 < cell.x <= mid_x and 0 < cell.y <= mid_y
        ]
        area_b = [
            (cell, direction)
            for cell, direction in closed_walls
            if mid_x < cell.x < grid.width and mid_y < cell.y < grid.height
        ]
        area_c = [
            (cell, direction)
            for cell, direction in closed_walls
            if 0 < cell.x <= mid_x and mid_y < cell.y < grid.height
        ]
        area_d = [
            (cell, direction)
            for cell, direction in closed_walls
            if mid_x < cell.x < grid.width and 0 < cell.y <= mid_y
        ]
        areas = [area_a, area_b, area_c, area_d]
        for a in areas:
            if not a:
                continue
            cell, direction = random.choice(a)
            if not GeneratorImperfect._creates_open_area(
                grid,
                cell,
                direction,
            ):
                grid.open_wall(cell, direction)
                if renderer.animate():
                    renderer.display_cell(grid, cell)

    @staticmethod
    def _is_opened_3x3(grid: Grid, x: int, y: int) -> bool:
        return all(
            grid.get_wall_state(Cell(col, row), Direction.EAST)
            is WallState.OPEN
            for row in range(y, y + 3)
            for col in range(x, x + 2)
        ) and all(
            grid.get_wall_state(Cell(col, row), Direction.SOUTH)
            is WallState.OPEN
            for row in range(y, y + 2)
            for col in range(x, x + 3)
        )

    @staticmethod
    def _creates_open_area(
        grid: Grid,
        cell: Cell,
        direction: Direction,
    ) -> bool:
        """Temporarily check if opening area will create 3x3 area"""
        grid.open_wall(cell, direction)
        result = any(
            GeneratorImperfect._is_opened_3x3(grid, x, y)
            for x in range(max(0, cell.x - 2), min(grid.width - 2, cell.x + 1))
            for y in range(
                max(0, cell.y - 2),
                min(grid.height - 2, cell.y + 1),
            )
        )
        grid.close_wall(cell, direction)
        return result
