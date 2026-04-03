import sys
import time
from dataclasses import dataclass

from mazegen.cell import Cell
from mazegen.cell_marking import CellMarking
from mazegen.cell_value import CellValue
from mazegen.color import Color
from mazegen.direction import Direction
from mazegen.grid import Grid
from mazegen.render.base import Renderer
from mazegen.wall_state import WallState


class AsciiRenderer(Renderer):
    def __init__(self) -> None:
        self._writer = AnsiWriter()

    def write_cell(self, grid: Grid, cell: Cell) -> None:
        color = get_cell_color(grid, cell)

        self._writer.move_to_position(cell)
        self._writer.write_box(color, 2, 2)

    def write_wall(self, grid: Grid, cell: Cell, direction: Direction) -> None:
        color = get_wall_color(grid, cell, direction)

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
                        self._writer.write_color_pixel(get_corner_color())
                    self._writer.write_color_pixel(
                        get_wall_color(grid, cell, Direction.NORTH),
                        2,
                    )
                    self._writer.write_color_pixel(get_corner_color())
                self._writer.write("\n")

            for _ in range(2):
                for x in range(grid.width):
                    cell = Cell(x, y)
                    if x == 0:
                        self._writer.write_color_pixel(
                            get_wall_color(
                                grid,
                                cell,
                                Direction.WEST,
                            ),
                            1,
                        )
                    self._writer.write_color_pixel(
                        get_cell_color(grid, cell),
                        2,
                    )
                    self._writer.write_color_pixel(
                        get_wall_color(
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
                    self._writer.write_color_pixel(get_corner_color())
                self._writer.write_color_pixel(
                    get_wall_color(grid, cell, Direction.SOUTH),
                    2,
                )
                self._writer.write_color_pixel(get_corner_color())
            self._writer.write("\n")

    def display_cell(self, grid: Grid, cell: Cell) -> None:
        start = time.perf_counter()
        self.write_cell(grid, cell)
        for direction in Direction:
            self.write_wall(grid, cell, direction)
        duration = time.perf_counter() - start

        self.write_duration(grid, duration)

        self._writer.flush()

        duration = time.perf_counter() - start
        time.sleep(max(0, 0.001 - duration))

    def display_grid(self, grid: Grid) -> None:
        start = time.perf_counter()
        self.write_grid(grid)
        duration = time.perf_counter() - start

        self.write_duration(grid, duration)

        self._writer.flush()

        duration = time.perf_counter() - start
        time.sleep(max(0, 0.500 - duration))

    def write_duration(self, grid: Grid, duration: float) -> None:
        self._writer.move_to_position(Cell(0, grid.height), 0, -2)
        self._writer.write_current_position()
        self._writer.write_clear_line()
        self._writer.write_color_reset()
        self._writer.write(f"rendering frame took {duration * 1000:.3f} ms\n")


def get_cell_color(grid: Grid, cell: Cell) -> Color:
    grid.validate_coordinate(cell)

    marking = grid.get_cell_marking(cell)
    value = grid.get_cell_value(cell)

    if value is not CellValue.NONE:
        return value.into_color()

    if marking is CellMarking.MARKED:
        return marking.into_color()

    return Color.BLACK


def get_wall_color(grid: Grid, cell: Cell, direction: Direction) -> Color:
    grid.validate_coordinate(cell)

    if grid.get_wall_state(cell, direction) is WallState.CLOSED:
        return Color.WHITE

    neighbor = grid.get_neighbor_cell(cell, direction)
    if neighbor is None:
        return Color.BLACK

    marking = grid.get_cell_marking(cell)
    value = grid.get_cell_value(cell)
    neighbor_marking = grid.get_cell_marking(neighbor)
    neighbor_value = grid.get_cell_value(neighbor)

    if value == neighbor_value and value is not CellValue.NONE:
        return value.into_color()

    if (
        marking is CellMarking.MARKED
        and neighbor_marking is CellMarking.MARKED
        and (value is CellValue.NONE or neighbor_value is CellValue.NONE)
    ):
        return marking.into_color()

    return max(value, neighbor_value).into_color()


def get_corner_color() -> Color:
    return Color.WHITE


@dataclass
class AnsiWriter:
    _buffer: str = ""
    _line: int = 1
    _column: int = 1

    def move_to_position(
        self,
        cell: Cell,
        line_offset: int = 0,
        column_offset: int = 0,
    ) -> None:
        self._line = cell.y * 3 + 2 + line_offset
        self._column = cell.x * 6 + 3 + column_offset

    def write(self, string: str) -> None:
        self._buffer += string

    def prepend_write(self, string: str) -> None:
        self._buffer = string + self._buffer

    def write_clear_screen(self) -> None:
        self.write("\033[2J\033[H")

    def write_clear_line(self) -> None:
        self.write("\033[2K")

    def write_cursor_up(self, lines: int) -> None:
        self.write(f"\033[{lines}A")

    def write_cursor_down(self, lines: int) -> None:
        self.write(f"\033[{lines}B")

    def write_cursor_forward(self, columns: int) -> None:
        self.write(f"\033[{columns}C")

    def write_cursor_backward(self, columns: int) -> None:
        self.write(f"\033[{columns}D")

    def write_cursor_position(self, line: int, column: int) -> None:
        self.write(f"\033[{line};{column}H")

    def write_current_position(self) -> None:
        self.write_cursor_position(self._line, self._column)

    def write_color_pixel(self, color: Color, width: int = 1) -> None:
        PIXEL = "██"
        self.write(color.escape_code())
        self.write(PIXEL * width)

    def write_color_reset(self) -> None:
        self.write(Color.reset())

    def write_box(self, color: Color, width: int, height: int) -> None:
        self.write_current_position()

        for i in range(height):
            if i > 0:
                self.write_cursor_down(1)
                self.write_cursor_backward(2 * width)

            self.write_color_pixel(color, width)

    def flush(self) -> None:
        sys.stdout.write(self._buffer)
        sys.stdout.flush()
        self._buffer = ""
