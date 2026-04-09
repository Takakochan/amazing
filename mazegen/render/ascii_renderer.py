import time

from mazegen.ansi_writer import AnsiWriter
from mazegen.cell import Cell
from mazegen.cell_marking import CellMarking
from mazegen.cell_value import CellValue
from mazegen.color import Color
from mazegen.direction import Direction
from mazegen.grid import Grid
from mazegen.render.base import Renderer
from mazegen.wall_state import WallState


class AsciiRenderer(Renderer):
    def __init__(self, animation_speed: int) -> None:
        self._animation_speed = animation_speed
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

    def write_duration(self, grid: Grid, duration: float) -> None:
        self._writer.move_to_position(Cell(0, grid.height), 0, -2)
        self._writer.write_current_position()
        self._writer.write_clear_line()
        self._writer.write_color_reset()
        self._writer.write(f"rendering frame took {duration * 1000:.3f} ms\n")

    def display_cell(self, grid: Grid, cell: Cell) -> None:
        start = time.perf_counter()

        self.write_cell(grid, cell)
        for direction in Direction:
            self.write_wall(grid, cell, direction)

        # self.write_duration(grid, time.perf_counter() - start)

        self._writer.flush()

        time.sleep(
            max(
                0,
                1.0 / self._animation_speed - (time.perf_counter() - start),
            ),
        )

    def display_grid(self, grid: Grid) -> None:
        start = time.perf_counter()

        self.write_grid(grid)

        # self.write_duration(grid, time.perf_counter() - start)

        self._writer.flush()

        time.sleep(
            max(
                0,
                1.0 / self._animation_speed - (time.perf_counter() - start),
            ),
        )


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
