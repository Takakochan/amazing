import time
from dataclasses import dataclass, field
from typing import Self

from color import Color
from config import Config
from mazegen.ansi_writer import AnsiWriter
from mazegen.cell import Cell
from mazegen.cell_marking import CellMarking
from mazegen.cell_value import CellValue
from mazegen.direction import Direction
from mazegen.grid import Grid
from mazegen.render.base import Renderer
from mazegen.render.config import RenderConfig
from mazegen.wall_state import WallState


@dataclass
class AsciiRenderer(Renderer):
    _config: RenderConfig
    _writer: AnsiWriter = field(default_factory=AnsiWriter)
    _show_solution: bool = True

    @classmethod
    def from_config(cls, config: Config) -> Self:
        return cls(RenderConfig.from_config(config))

    def animate(self) -> bool:
        return self._config.animation

    def show_solution(self) -> bool:
        if not self._show_solution:
            self._show_solution = True
            return True

        return False

    def hide_solution(self) -> bool:
        if self._show_solution:
            self._show_solution = False
            return True

        return False

    def get_cell_color(self, grid: Grid, cell: Cell) -> Color:
        grid.validate_coordinate(cell)

        marking = grid.get_cell_marking(cell)
        value = grid.get_cell_value(cell)

        if value is CellValue.SOLUTION and self._show_solution:
            return value.into_color(self._config)

        if value is not CellValue.NONE and value is not CellValue.SOLUTION:
            return value.into_color(self._config)

        if marking is CellMarking.MARKED:
            return marking.into_color(self._config)

        return self._config.background_color

    def get_wall_color(
        self,
        grid: Grid,
        cell: Cell,
        direction: Direction,
    ) -> Color:
        grid.validate_coordinate(cell)

        if grid.get_wall_state(cell, direction) is WallState.CLOSED:
            return self._config.wall_color

        neighbor = grid.get_neighbor_cell(cell, direction)
        if neighbor is None:
            return self._config.background_color

        marking = grid.get_cell_marking(cell)
        value = grid.get_cell_value(cell)
        neighbor_marking = grid.get_cell_marking(neighbor)
        neighbor_value = grid.get_cell_value(neighbor)

        if (
            value == neighbor_value
            and value is CellValue.SOLUTION
            and self._show_solution
        ):
            return value.into_color(self._config)

        if (
            value == neighbor_value
            and value is not CellValue.NONE
            and value is not CellValue.SOLUTION
        ):
            return value.into_color(self._config)

        if (
            marking is CellMarking.MARKED
            and neighbor_marking is CellMarking.MARKED
            and (value is CellValue.NONE or neighbor_value is CellValue.NONE)
        ):
            return marking.into_color(self._config)

        max_value = max(value, neighbor_value)
        if max_value is CellValue.SOLUTION and self._show_solution:
            return max_value.into_color(self._config)

        return CellValue.NONE.into_color(self._config)

    def get_corner_color(self) -> Color:
        return self._config.wall_color

    def write_cell(self, grid: Grid, cell: Cell) -> None:
        color = self.get_cell_color(grid, cell)

        self._writer.move_to_position(cell)
        self._writer.write_box(color, 2, 2)

    def write_wall(self, grid: Grid, cell: Cell, direction: Direction) -> None:
        color = self.get_wall_color(grid, cell, direction)

        match direction:
            case Direction.NORTH:
                self._writer.move_to_position(cell, -1, 0)
                self._writer.write_box(color, 2, 1)
            case Direction.EAST:
                self._writer.move_to_position(cell, 0, 4)
                self._writer.write_box(color, 1, 2)
            case Direction.SOUTH:
                self._writer.move_to_position(cell, 2, 0)
                self._writer.write_box(color, 2, 1)
            case Direction.WEST:
                self._writer.move_to_position(cell, 0, -2)
                self._writer.write_box(color, 1, 2)

    def write_grid(self, grid: Grid) -> None:
        self._writer.write_clear_screen()

        for y in range(grid.height):
            if y == 0:
                for x in range(grid.width):
                    cell = Cell(x, y)
                    if x == 0:
                        self._writer.write_color_pixel(self.get_corner_color())
                    self._writer.write_color_pixel(
                        self.get_wall_color(grid, cell, Direction.NORTH),
                        2,
                    )
                    self._writer.write_color_pixel(self.get_corner_color())
                self._writer.write("\n")

            for _ in range(2):
                for x in range(grid.width):
                    cell = Cell(x, y)
                    if x == 0:
                        self._writer.write_color_pixel(
                            self.get_wall_color(
                                grid,
                                cell,
                                Direction.WEST,
                            ),
                            1,
                        )
                    self._writer.write_color_pixel(
                        self.get_cell_color(grid, cell),
                        2,
                    )
                    self._writer.write_color_pixel(
                        self.get_wall_color(
                            grid,
                            cell,
                            Direction.EAST,
                        ),
                        1,
                    )
                self._writer.write("\n")

            for x in range(grid.width):
                cell = Cell(x, y)
                if x == 0:
                    self._writer.write_color_pixel(self.get_corner_color())
                self._writer.write_color_pixel(
                    self.get_wall_color(grid, cell, Direction.SOUTH),
                    2,
                )
                self._writer.write_color_pixel(self.get_corner_color())
            self._writer.write("\n")

    def display_cell(self, grid: Grid, cell: Cell) -> None:
        start = time.perf_counter()

        self.write_cell(grid, cell)
        for direction in Direction:
            self.write_wall(grid, cell, direction)

        self._writer.flush()

        time.sleep(
            max(
                0,
                1.0 / self._config.animation_speed
                - (time.perf_counter() - start),
            ),
        )

    def display_grid(self, grid: Grid) -> None:
        start = time.perf_counter()

        self.write_grid(grid)

        self._writer.flush()

        time.sleep(
            max(
                0,
                1.0 / self._config.animation_speed
                - (time.perf_counter() - start),
            ),
        )

    def random_color(self, grid: Grid) -> None:
        self._config.randomize()
        self.display_grid(grid)
