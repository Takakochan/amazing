import random

from src.mazegen.cell import Cell
from src.mazegen.direction import Direction
from src.mazegen.generators.base import Generator
from src.mazegen.generators.dfs import GeneratorDFS
from src.mazegen.grid import Grid
from src.mazegen.render.base import Renderer
from src.mazegen.wall_state import WallState


class GeneratorImperfect(Generator):
    def generate(
        self,
        grid: Grid,
        seed: int | None,
        renderer: Renderer,
    ) -> int:
        self._foo = None

        generator = GeneratorDFS()
        seed = generator.generate(grid, seed, renderer)
        closed_walls = grid.get_collect_closed_walls()
        open_walls_by_areas(grid, renderer, closed_walls)

        return seed


def open_walls_by_areas(
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

    for area in [area_a, area_b, area_c, area_d]:
        if not area:
            continue

        cell, direction = random.choice(area)

        if creates_open_area(
            grid,
            cell,
            direction,
        ):
            continue

        grid.open_wall(cell, direction)

        if renderer.animate():
            renderer.display_cell(grid, cell)


def creates_open_area(
    grid: Grid,
    cell: Cell,
    direction: Direction,
) -> bool:
    """Temporarily check if opening area will create 3x3 area"""

    grid.open_wall(cell, direction)

    result = any(
        is_opened_3x3(grid, x, y)
        for x in range(max(0, cell.x - 2), min(grid.width - 2, cell.x + 1))
        for y in range(
            max(0, cell.y - 2),
            min(grid.height - 2, cell.y + 1),
        )
    )

    grid.close_wall(cell, direction)

    return result


def is_opened_3x3(grid: Grid, x: int, y: int) -> bool:
    east_walls_open = all(
        grid.get_wall_state(Cell(col, row), Direction.EAST) is WallState.OPEN
        for row in range(y, y + 3)
        for col in range(x, x + 2)
    )
    south_walls_open = all(
        grid.get_wall_state(Cell(col, row), Direction.SOUTH) is WallState.OPEN
        for row in range(y, y + 2)
        for col in range(x, x + 3)
    )

    return east_walls_open and south_walls_open
