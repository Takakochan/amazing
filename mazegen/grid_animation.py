import sys
import time

from mazegen.cell import Cell
from mazegen.cell_marking import CellMarking
from mazegen.cell_value import CellValue
from mazegen.color import Color
from mazegen.direction import Direction
from mazegen.grid import Grid
from mazegen.wall_state import WallState


class GridAnimation(Grid):
    CORNER_WALL_COLOR = Color.WHITE

    def _get_cell_color(self, cell: Cell) -> Color:
        self._validate_coordinate(cell)

        marking = self._get_cell_marking(cell)
        value = self._get_cell_value(cell)

        if value is not CellValue.NONE:
            return value.into_color()

        if marking is CellMarking.MARKED:
            return marking.into_color()

        return Color.BLACK

    def _get_wall_color(self, cell: Cell, direction: Direction) -> Color:
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

    def _recreate_buffer(self) -> str:
        buffer = ""

        for y in range(self.height):
            if y == 0:
                for x in range(self.width):
                    cell = Cell(x, y)
                    if x == 0:
                        buffer += self.CORNER_WALL_COLOR.to_string()
                    buffer += (
                        self._get_wall_color(cell, Direction.NORTH).to_string()
                        * 2
                    )
                    buffer += self.CORNER_WALL_COLOR.to_string()
                buffer += "\n"

            for _ in range(2):
                for x in range(self.width):
                    cell = Cell(x, y)
                    if x == 0:
                        buffer += self._get_wall_color(
                            cell,
                            Direction.WEST,
                        ).to_string()
                    buffer += self._get_cell_color(cell).to_string() * 2
                    buffer += self._get_wall_color(
                        cell,
                        Direction.EAST,
                    ).to_string()
                buffer += "\n"

            for x in range(self.width):
                cell = Cell(x, y)
                if x == 0:
                    buffer += self.CORNER_WALL_COLOR.to_string()
                buffer += (
                    self._get_wall_color(cell, Direction.SOUTH).to_string() * 2
                )
                buffer += self.CORNER_WALL_COLOR.to_string()
            buffer += "\n"

        return buffer

    def display(self) -> None:
        start = time.perf_counter()
        buffer = self._recreate_buffer()
        duration = time.perf_counter() - start

        sys.stdout.write("\033[2J\033[H")
        sys.stdout.write(f"duration: {duration * 1000:.3f}\n")
        sys.stdout.write(buffer)
        sys.stdout.flush()

        left = start + 0.025 - time.perf_counter()
        if left > 0:
            time.sleep(left)
