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

        closed_walls = grid.get_closed_walls()
        random.shuffle(closed_walls)

        for cell, direction in closed_walls:
            if random.random() * 3 > 1:
                continue

            if creates_open_area(grid, cell, direction):
                continue

            grid.open_wall(cell, direction)

            if renderer.animate():
                renderer.display_cell(grid, cell)

        return seed


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
