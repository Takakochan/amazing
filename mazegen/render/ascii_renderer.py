import time

from mazegen.cell import Cell
from mazegen.cell_marking import CellMarking
from mazegen.cell_value import CellValue
from mazegen.color import Color
from mazegen.direction import Direction
from mazegen.grid import Grid
from mazegen.render.ansi_writer import AnsiWriter
from mazegen.render.base import Renderer
from mazegen.wall_state import WallState


class AsciiRenderer(Renderer):
    def __init__(self, width: int, height: int) -> None:
        self._grid = Grid(width, height)
        self._writer = AnsiWriter()

    def get_cell_color(self, cell: Cell) -> Color:
        self._grid.validate_coordinate(cell)

        marking = self._grid.get_cell_marking(cell)
        value = self._grid.get_cell_value(cell)

        if value is not CellValue.NONE:
            return value.into_color()

        if marking is CellMarking.MARKED:
            return marking.into_color()

        return Color.BLACK

    def get_wall_color(self, cell: Cell, direction: Direction) -> Color:
        self._grid.validate_coordinate(cell)

        if self._grid.get_wall_state(cell, direction) is WallState.CLOSED:
            return Color.WHITE

        neighbor = self._grid.get_neighbor_cell(cell, direction)
        if neighbor is None:
            return Color.BLACK

        marking = self._grid.get_cell_marking(cell)
        value = self._grid.get_cell_value(cell)
        neighbor_marking = self._grid.get_cell_marking(neighbor)
        neighbor_value = self._grid.get_cell_value(neighbor)

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
            Cell(x, y)
            for x in range(self._grid.width)
            for y in range(self._grid.height)
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

        # self._writer.reset()
        self._writer.write_clear_screen()

        self.write_all()

        duration = time.perf_counter() - start
        self.write_duration(duration)

        self._writer.flush()

        # if duration < 0.010:
        #     time.sleep(0.010 - duration)
