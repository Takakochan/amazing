from dataclasses import dataclass
from enum import Enum, auto

from mazegen.cell import Cell
from mazegen.cell_state import CellState
from mazegen.cell_value import CellValue
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
        self.unmark_cells()
        self.close_walls()

    def set_forty_two_pattern(self, avoid_cells: list[Cell]) -> None:
        self.unmark_cells()

        try:
            cells = get_forty_two_cells(self.width, self.height, avoid_cells)
        except FortyTwoPatternError as error:
            raise error

        for cell in cells:
            self.set_cell_value(cell, CellValue.FORTY_TWO)

            # for neighbor in self.get_unmarked_neighbors(cell):
            #     if neighbor not in cells:
            #         continue
            #
            #     try:
            #         direction = cell.get_direction_to_neighbor(neighbor)
            #     except RuntimeError as error:
            #         raise error
            #
            #     self.open_wall(cell, direction)

    def _validate_coordinate(
        self,
        cell: Cell,
    ) -> None:
        cell.validate(self.width, self.height)

    def unmark_cells(self) -> None:
        self._cells = [
            [CellValue.UNMARKED for _x in range(self.width)]
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

    def unmark_marked_cells(self) -> None:
        for cell in [
            cell
            for cell in (
                Cell(x, y)
                for x in range(self.width)
                for y in range(self.height)
            )
            if self._get_cell_value(cell) == CellValue.MARKED
        ]:
            self.set_cell_value(cell, CellValue.UNMARKED)

    def _get_cell_value(self, cell: Cell) -> CellValue:
        self._validate_coordinate(cell)

        return self._cells[cell.y][cell.x]

    def set_cell_value(self, cell: Cell, value: CellValue) -> None:
        self._validate_coordinate(cell)

        self._cells[cell.y][cell.x] = value

    def unmark_cell(self, cell: Cell) -> None:
        self._validate_coordinate(cell)

        self.set_cell_value(cell, CellValue.UNMARKED)

    def mark_cell(self, cell: Cell) -> None:
        self._validate_coordinate(cell)

        self.set_cell_value(cell, CellValue.MARKED)

    def _get_neighbor_cell(
        self,
        cell: Cell,
        direction: Direction,
    ) -> tuple[Cell, CellValue] | None:
        self._validate_coordinate(cell)

        match direction:
            case Direction.NORTH:
                if cell.y == 0:
                    return None
                neighbor = Cell(cell.x, cell.y - 1)
                return neighbor, self._get_cell_value(neighbor)
            case Direction.EAST:
                if cell.x == self.width - 1:
                    return None
                neighbor = Cell(cell.x + 1, cell.y)
                return neighbor, self._get_cell_value(neighbor)
            case Direction.SOUTH:
                if cell.y == self.height - 1:
                    return None
                neighbor = Cell(cell.x, cell.y + 1)
                return neighbor, self._get_cell_value(neighbor)
            case Direction.WEST:
                if cell.x == 0:
                    return None
                neighbor = Cell(cell.x - 1, cell.y)
                return neighbor, self._get_cell_value(neighbor)

    def _get_neighbor_cells(
        self,
        cell: Cell,
    ) -> list[tuple[Cell, CellValue]]:
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
            for neighbor, value in self._get_neighbor_cells(cell)
            if value == CellValue.UNMARKED
        ]

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
        match self._get_cell_value(cell):
            case CellValue.UNMARKED:
                print_pixel()
                print_pixel()
            case CellValue.MARKED:
                print_pixel(Color.BLUE)
                print_pixel(Color.BLUE)
            case CellValue.ENTRY:
                print_pixel(Color.GREEN)
                print_pixel(Color.GREEN)
            case CellValue.EXIT:
                print_pixel(Color.RED)
                print_pixel(Color.RED)
            case CellValue.FORTY_TWO:
                print_pixel(Color.YELLOW)
                print_pixel(Color.YELLOW)

    def _print_wall(self, cell: Cell, direction: Direction) -> None:
        self._validate_coordinate(cell)

        match (self._get_wall_state(cell, direction), direction):
            case (WallState.OPEN, Direction.NORTH | Direction.SOUTH):
                print_pixel()
                print_pixel()
            case (WallState.OPEN, Direction.WEST | Direction.EAST):
                print_pixel()
            case (WallState.CLOSED, Direction.NORTH | Direction.SOUTH):
                print_pixel(Color.BLACK)
                print_pixel(Color.BLACK)
            case (WallState.CLOSED, Direction.WEST | Direction.EAST):
                print_pixel(Color.BLACK)

    def display(self) -> None:
        for y in range(self.height):
            if y == 0:
                for x in range(self.width):
                    cell = Cell(x, y)
                    if x == 0:
                        print_pixel(Color.BLACK)
                    self._print_wall(cell, Direction.NORTH)
                    print_pixel(Color.BLACK)

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
                    print_pixel(Color.BLACK)
                self._print_wall(cell, Direction.SOUTH)
                print_pixel(Color.BLACK)

            print()


class Color(Enum):
    NONE = auto()
    BLACK = auto()
    RED = auto()
    GREEN = auto()
    YELLOW = auto()
    BLUE = auto()
    MAGENTA = auto()
    CYAN = auto()
    WHITE = auto()


def print_pixel(color: Color = Color.NONE) -> None:
    match color:
        case Color.NONE:
            print("██", end="")
        case Color.BLACK:
            print("\033[30m██\033[0m", end="")
        case Color.RED:
            print("\033[31m██\033[0m", end="")
        case Color.GREEN:
            print("\033[32m██\033[0m", end="")
        case Color.YELLOW:
            print("\033[33m██\033[0m", end="")
        case Color.BLUE:
            print("\033[34m██\033[0m", end="")
        case Color.MAGENTA:
            print("\033[35m██\033[0m", end="")
        case Color.CYAN:
            print("\033[36m██\033[0m", end="")
        case Color.WHITE:
            print("\033[37m██\033[0m", end="")
