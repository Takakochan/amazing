from dataclasses import dataclass
from time import sleep

from mazegen.cell import Cell
from mazegen.cell_marking import CellMarking
from mazegen.cell_state import CellState
from mazegen.cell_value import CellValue
from mazegen.color import Color, print_pixel
from mazegen.direction import Direction
from mazegen.wall_state import WallState

FORTY_TWO = [
    [1, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1],
]

FORTY_TWO_WIDTH = len(FORTY_TWO[0])
FORTY_TWO_HEIGHT = len(FORTY_TWO)

FORTY_TWO_OFFSETS = [
    (0, 0),
    (-1, 0),
    (0, -1),
    (-1, -1),
    (-1, 1),
    (1, -1),
    (0, 1),
    (1, 0),
    (1, 1),
    (-2, 0),
    (0, -2),
    (-2, -1),
    (-1, -2),
    (-2, -2),
    (-2, 1),
    (1, -2),
    (-2, 2),
    (2, -2),
    (-1, 2),
    (2, -1),
    (0, 2),
    (2, 0),
    (1, 2),
    (2, 1),
    (2, 2),
]


class FortyTwoPatternError(Exception):
    pass


def get_forty_two_cells_at(
    width: int,
    height: int,
    x_start: int,
    y_start: int,
    avoid_cells: list[Cell],
) -> list[Cell] | None:
    forty_two_cells = [
        Cell(x_start + x, y_start + y)
        for x in range(FORTY_TWO_WIDTH)
        for y in range(FORTY_TWO_HEIGHT)
        if FORTY_TWO[y][x] == 1
    ]

    if any(
        not cell.is_in_range(width, height)
        or cell.is_at_edge(width, height)
        or cell in avoid_cells
        for cell in forty_two_cells
    ):
        return None

    return forty_two_cells


def get_forty_two_cells(
    width: int,
    height: int,
    avoid_cells: list[Cell],
) -> list[Cell]:
    if width < FORTY_TWO_WIDTH + 2:
        raise FortyTwoPatternError(
            f"width should be at least `{FORTY_TWO_WIDTH + 2}`: `{width}`",
        )

    if height < FORTY_TWO_HEIGHT + 2:
        raise FortyTwoPatternError(
            f"height should be at least `{FORTY_TWO_HEIGHT + 2}`: `{height}`",
        )

    x_start = (width - FORTY_TWO_WIDTH) // 2
    y_start = (height - FORTY_TWO_HEIGHT) // 2

    for x_offset, y_offset in FORTY_TWO_OFFSETS:
        if abs(x_offset) == 1 and width < FORTY_TWO_WIDTH + 3:
            continue

        if abs(y_offset) == 1 and height < FORTY_TWO_HEIGHT + 3:
            continue

        cells = get_forty_two_cells_at(
            width,
            height,
            x_start + x_offset,
            y_start + y_offset,
            avoid_cells,
        )

        if cells is None:
            continue

        return cells

    raise FortyTwoPatternError("the maze is too small")


@dataclass
class Grid:
    width: int
    height: int

    def __post_init__(self) -> None:
        self.reset_cell_markings()
        self.reset_cell_values()
        self.close_walls()
        self.unset_parents()

    def set_forty_two_pattern(self, avoid_cells: list[Cell]) -> None:
        self.reset_cell_markings()

        try:
            cells = get_forty_two_cells(self.width, self.height, avoid_cells)
        except FortyTwoPatternError as error:
            raise error

        for cell in cells:
            self.set_cell_value(cell, CellValue.FORTY_TWO)
            self.mark_cell(cell)

            for neighbor in self.get_unmarked_neighbors(cell):
                if neighbor not in cells:
                    continue

                try:
                    direction = cell.get_direction_to_neighbor(neighbor)
                except RuntimeError as error:
                    raise error

                self.open_wall(cell, direction)

    def _validate_coordinate(
        self,
        cell: Cell,
    ) -> None:
        cell.validate(self.width, self.height)

    def reset_cell_markings(self) -> None:
        self._cell_markings = [
            [CellMarking.UNMARKED for _x in range(self.width)]
            for _y in range(self.height)
        ]

    def reset_cell_values(self) -> None:
        self._cell_values = [
            [CellValue.NONE for _x in range(self.width)]
            for _y in range(self.height)
        ]

    def close_walls(self) -> None:
        self._north_walls = [
            [WallState.CLOSED for _x in range(self.width)]
            for _y in range(self.height + 1)
        ]

        self._west_walls = [
            [WallState.CLOSED for _x in range(self.width + 1)]
            for _y in range(self.height)
        ]

    def unset_parents(self) -> None:
        self._parents: list[list[Cell | None]] = [
            [None for _x in range(self.width)] for _y in range(self.height)
        ]

    def _get_cell_marking(self, cell: Cell) -> CellMarking:
        self._validate_coordinate(cell)

        return self._cell_markings[cell.y][cell.x]

    def _get_cell_value(self, cell: Cell) -> CellValue:
        self._validate_coordinate(cell)

        return self._cell_values[cell.y][cell.x]

    def _set_cell_marking(self, cell: Cell, value: CellMarking) -> None:
        self._validate_coordinate(cell)

        self._cell_markings[cell.y][cell.x] = value

    def unmark_cell(self, cell: Cell) -> None:
        self._validate_coordinate(cell)

        self._set_cell_marking(cell, CellMarking.UNMARKED)

    def mark_cell(self, cell: Cell) -> None:
        self._validate_coordinate(cell)

        self._set_cell_marking(cell, CellMarking.MARKED)

    def set_cell_value(self, cell: Cell, value: CellValue) -> None:
        self._validate_coordinate(cell)

        self._cell_values[cell.y][cell.x] = value

    def get_parent(self, child: Cell) -> Cell | None:
        return self._parents[child.y][child.x]

    def set_parent(self, child: Cell, parent: Cell) -> None:
        self._parents[child.y][child.x] = parent

    def _get_neighbor_cell(
        self,
        cell: Cell,
        direction: Direction,
    ) -> Cell | None:
        self._validate_coordinate(cell)

        match direction:
            case Direction.NORTH:
                if cell.y == 0:
                    return None
                return Cell(cell.x, cell.y - 1)
            case Direction.EAST:
                if cell.x == self.width - 1:
                    return None
                return Cell(cell.x + 1, cell.y)
            case Direction.SOUTH:
                if cell.y == self.height - 1:
                    return None
                return Cell(cell.x, cell.y + 1)
            case Direction.WEST:
                if cell.x == 0:
                    return None
                return Cell(cell.x - 1, cell.y)

    def _get_neighbor_cells(
        self,
        cell: Cell,
    ) -> list[Cell]:
        return [
            neighbor
            for neighbor in (
                self._get_neighbor_cell(cell, direction)
                for direction in Direction
            )
            if neighbor is not None
        ]

    def get_unmarked_neighbors(
        self,
        cell: Cell,
    ) -> list[Cell]:
        return [
            neighbor
            for neighbor in self._get_neighbor_cells(cell)
            if self._get_cell_marking(neighbor) == CellMarking.UNMARKED
        ]

    def get_reachable_unmarked_neighbors(
        self,
        cell: Cell,
    ) -> list[Cell]:
        neighbors = []

        for neighbor in self.get_unmarked_neighbors(cell):
            try:
                direction = cell.get_direction_to_neighbor(neighbor)
            except RuntimeError:
                continue

            wall_state = self._get_wall_state(cell, direction)

            if wall_state is WallState.OPEN:
                neighbors.append(neighbor)

        return neighbors

    def _get_wall_state(
        self,
        cell: Cell,
        direction: Direction,
    ) -> WallState:
        self._validate_coordinate(cell)

        match direction:
            case Direction.NORTH:
                return self._north_walls[cell.y][cell.x]
            case Direction.EAST:
                return self._west_walls[cell.y][cell.x + 1]
            case Direction.SOUTH:
                return self._north_walls[cell.y + 1][cell.x]
            case Direction.WEST:
                return self._west_walls[cell.y][cell.x]

    def _set_wall_state(
        self,
        cell: Cell,
        direction: Direction,
        state: WallState,
    ) -> None:
        self._validate_coordinate(cell)

        match direction:
            case Direction.NORTH:
                self._north_walls[cell.y][cell.x] = state
            case Direction.EAST:
                self._west_walls[cell.y][cell.x + 1] = state
            case Direction.SOUTH:
                self._north_walls[cell.y + 1][cell.x] = state
            case Direction.WEST:
                self._west_walls[cell.y][cell.x] = state

    def open_wall(self, cell: Cell, direction: Direction) -> None:
        self._set_wall_state(cell, direction, WallState.OPEN)

    def close_wall(self, cell: Cell, direction: Direction) -> None:
        self._set_wall_state(cell, direction, WallState.CLOSED)

    def _get_cell_state(self, cell: Cell) -> CellState:
        self._validate_coordinate(cell)

        north = self._get_wall_state(cell, Direction.NORTH)
        east = self._get_wall_state(cell, Direction.EAST)
        south = self._get_wall_state(cell, Direction.SOUTH)
        west = self._get_wall_state(cell, Direction.WEST)

        return CellState(north, east, south, west)

    def get_all_cell_states(self) -> list[list[CellState]]:
        return [
            [self._get_cell_state(Cell(x, y)) for x in range(self.width)]
            for y in range(self.height)
        ]

    def into_file_format(self) -> str:
        return (
            "\n".join([
                "".join([cell.to_hex() for cell in cell_list])
                for cell_list in self.get_all_cell_states()
            ])
            + "\n"
        )

    def _print_cell_value(self, cell: Cell) -> None:
        marking = self._get_cell_marking(cell)
        value = self._get_cell_value(cell)

        if value is not CellValue.NONE:
            color = value.into_color()
        elif marking is CellMarking.MARKED:
            color = marking.into_color()
        else:
            color = Color.BLACK

        print_pixel(color)
        print_pixel(color)

    def _print_wall(self, cell: Cell, direction: Direction) -> None:
        self._validate_coordinate(cell)

        def get_color() -> Color:
            match self._get_wall_state(cell, direction):
                case WallState.OPEN:
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
                        and (
                            value is CellValue.NONE
                            or neighbor_value is CellValue.NONE
                        )
                    ):
                        return marking.into_color()

                    if value > neighbor_value:
                        return value.into_color()

                    return neighbor_value.into_color()
                case WallState.CLOSED:
                    return Color.WHITE

        color = get_color()

        match direction:
            case Direction.NORTH | Direction.SOUTH:
                print_pixel(color)
                print_pixel(color)
            case Direction.WEST | Direction.EAST:
                print_pixel(color)

    def display(self) -> None:
        print("\033[2J")

        for y in range(self.height):
            if y == 0:
                for x in range(self.width):
                    cell = Cell(x, y)
                    if x == 0:
                        print_pixel(Color.WHITE)
                    self._print_wall(cell, Direction.NORTH)
                    print_pixel(Color.WHITE)

                print()

            for x in range(self.width):
                cell = Cell(x, y)
                if x == 0:
                    self._print_wall(cell, Direction.WEST)
                self._print_cell_value(cell)
                self._print_wall(cell, Direction.EAST)

            print()

            for x in range(self.width):
                cell = Cell(x, y)
                if x == 0:
                    self._print_wall(cell, Direction.WEST)
                self._print_cell_value(cell)
                self._print_wall(cell, Direction.EAST)

            print()

            for x in range(self.width):
                cell = Cell(x, y)
                if x == 0:
                    print_pixel(Color.WHITE)
                self._print_wall(cell, Direction.SOUTH)
                print_pixel(Color.WHITE)

            print()

        sleep(0.050)
