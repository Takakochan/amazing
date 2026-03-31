import sys
import time
from dataclasses import dataclass

from mazegen.cell import Cell
from mazegen.cell_marking import CellMarking
from mazegen.cell_value import CellValue
from mazegen.color import Color
from mazegen.direction import Direction
from mazegen.grid import Grid
from mazegen.wall_state import WallState

PIXEL = "██"


@dataclass
class AnsiWriter:
    _line: int = 1
    _column: int = 1

    def __init__(self) -> None:
        self.reset()

    def move_to_position(
        self,
        cell: Cell,
        line_offset: int = 0,
        column_offset: int = 0,
    ) -> None:
        self._line = cell.y * 3 + 2 + line_offset
        self._column = cell.x * 6 + 3 + column_offset

    def reset(self) -> None:
        self._buffer = ""

    def write(self, string: str) -> None:
        self._buffer += string

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

    def write_box(self, color: Color, width: int, height: int) -> None:
        self.write_current_position()
        for i in range(height):
            if i > 0:
                self.write_cursor_down(1)
                self.write_cursor_backward(2 * width)
            self.write(color.escape_code() + PIXEL * width)

    def flush(self) -> None:
        sys.stdout.write(self._buffer)
        sys.stdout.flush()


class GridColorGetter(Grid):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)

    def get_cell_color(self, cell: Cell) -> Color:
        self._validate_coordinate(cell)

        marking = self._get_cell_marking(cell)
        value = self._get_cell_value(cell)

        if value is not CellValue.NONE:
            return value.into_color()

        if marking is CellMarking.MARKED:
            return marking.into_color()

        return Color.BLACK

    def get_wall_color(self, cell: Cell, direction: Direction) -> Color:
        self._validate_coordinate(cell)

        if self._get_wall_state(cell, direction) is WallState.CLOSED:
            return Color.WHITE

        neighbor = self._get_neighbor_cell(cell, direction)
        if neighbor is None:
            return Color.BLACK

        marking = self._get_cell_marking(cell)
        value = self._get_cell_value(cell)
        neighbor_marking = self._get_cell_marking(neighbor)
        neighbor_value = self._get_cell_value(neighbor)

        if value == neighbor_value and value is not CellValue.NONE:
            return value.into_color()

        if (
            marking is CellMarking.MARKED
            and neighbor_marking is CellMarking.MARKED
            and (value is CellValue.NONE or neighbor_value is CellValue.NONE)
        ):
            return marking.into_color()

        return max(value, neighbor_value).into_color()

    @staticmethod
    def get_corner_color() -> Color:
        return Color.WHITE


class GridDisplayer(GridColorGetter):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self._writer = AnsiWriter()

    def write_cell(self, cell: Cell) -> None:
        color = self.get_cell_color(cell)

        self._writer.move_to_position(cell)
        self._writer.write_box(color, 2, 2)

    def write_wall(self, cell: Cell, direction: Direction) -> None:
        color = self.get_wall_color(cell, direction)

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

    def write_corners(self, cell: Cell) -> None:
        color = self.get_corner_color()

        self._writer.move_to_position(cell, -1, -2)
        self._writer.write_box(color, 1, 1)
        self._writer.move_to_position(cell, -1, 4)
        self._writer.write_box(color, 1, 1)
        self._writer.move_to_position(cell, 2, -2)
        self._writer.write_box(color, 1, 1)
        self._writer.move_to_position(cell, 2, 4)
        self._writer.write_box(color, 1, 1)

    def write_cell_with_walls(self, cell: Cell) -> None:
        self.write_cell(cell)

        for direction in Direction:
            self.write_wall(cell, direction)

    def write_all(self) -> None:
        for cell in [
            Cell(x, y) for x in range(self.width) for y in range(self.height)
        ]:
            self.write_cell_with_walls(cell)
            self.write_corners(cell)

        self._writer.write("\n")

    def write_duration(self, duration: float) -> None:
        self._writer.write_cursor_position(1000, 1)
        self._writer.write_cursor_up(2)
        self._writer.write_clear_line()
        self._writer.write(
            f"{Color.reset()}duration: {duration * 1000:.3f} ms",
        )

    def display_cell(self, cell: Cell) -> None:
        start = time.perf_counter()
        self.write_cell_with_walls(cell)
        duration = time.perf_counter() - start
        self.write_duration(duration)
        self._writer.flush()

        # if duration < 0.010:
        #     time.sleep(0.010 - duration)

    def display(self) -> None:
        start = time.perf_counter()

        self._writer.reset()
        self._writer.write_clear_screen()

        self.write_all()

        duration = time.perf_counter() - start
        self.write_duration(duration)

        self._writer.flush()

        # if duration < 0.010:
        #     time.sleep(0.010 - duration)
