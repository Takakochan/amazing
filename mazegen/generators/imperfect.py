import random

from mazegen.cell import Cell
from mazegen.cell_value import CellValue
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
        generator = GeneratorDFS()
        generator.generate(grid, seed, renderer)
        closed_walls = self._collect_closed_walls(grid)
        self._open_random_walls(grid, renderer, closed_walls)
        return 0

    def _collect_closed_walls(self, grid: Grid) -> list:
        closed_walls = []
        for x in range(grid.width):
            for y in range(grid.height):
                cell = Cell(x, y)
                if (
                    y < grid.height - 1
                    and grid.get_wall_state(cell, Direction.SOUTH)
                    == WallState.CLOSED
                    and grid.get_cell_value(Cell(x, y + 1))
                    != CellValue.FORTY_TWO
                    and grid.get_cell_value(cell) != CellValue.FORTY_TWO
                ):
                    closed_walls.append((cell, Direction.SOUTH))
                if (
                    x > 0
                    and grid.get_wall_state(cell, Direction.WEST)
                    == WallState.CLOSED
                    and grid.get_cell_value(Cell(x - 1, y))
                    != CellValue.FORTY_TWO
                    and grid.get_cell_value(cell) != CellValue.FORTY_TWO
                ):
                    closed_walls.append((cell, Direction.WEST))
        return closed_walls

    def _open_random_walls(
        self,
        grid: Grid,
        renderer: Renderer,
        closed_walls: list,
        # ratio: float = 0.
    ) -> None:
        # count = max(1, int(len(closed_walls) * ratio))
        chosen = random.sample(closed_walls, min(5, len(closed_walls)))
        for cell, direction in chosen:
            grid.open_wall(cell, direction)
            renderer.display_cell(grid, cell)


"""
in grid.py
    def get_cell_value(self, cell: Cell) -> CellValue:
        self.validate_coordinate(cell)

        return self._cell_values[cell.y][cell.x]


    def get_wall_state(self, cell: Cell, direction: Direction) -> WallState:
        self.validate_coordinate(cell)

        match direction:
            case Direction.NORTH:
                return self._north_walls[cell.y][cell.x]
            case Direction.EAST:
                return self._west_walls[cell.y][cell.x + 1]
            case Direction.SOUTH:
                return self._north_walls[cell.y + 1][cell.x]
            case Direction.WEST:
                return self._west_walls[cell.y][cell.x]

"""
