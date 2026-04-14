from dataclasses import dataclass

from mazegen.cell import Cell
from mazegen.cell_marking import CellMarking
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

            for neighbor in [
                neighbor
                for neighbor in self.get_unmarked_neighbors(cell)
                if neighbor in cells
            ]:
                direction = cell.get_direction_to_neighbor(neighbor)
                self.open_wall(cell, direction)

    def validate_coordinate(self, cell: Cell) -> None:
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

    def get_cell_marking(self, cell: Cell) -> CellMarking:
        self.validate_coordinate(cell)

        return self._cell_markings[cell.y][cell.x]

    def get_cell_value(self, cell: Cell) -> CellValue:
        self.validate_coordinate(cell)

        return self._cell_values[cell.y][cell.x]

    def _set_cell_marking(self, cell: Cell, marking: CellMarking) -> None:
        self.validate_coordinate(cell)

        self._cell_markings[cell.y][cell.x] = marking

    # def unmark_cell(self, cell: Cell) -> None:
    #     self.validate_coordinate(cell)
    #
    #     self._set_cell_marking(cell, CellMarking.UNMARKED)

    def mark_cell(self, cell: Cell) -> None:
        self.validate_coordinate(cell)

        self._set_cell_marking(cell, CellMarking.MARKED)

    def set_cell_value(self, cell: Cell, value: CellValue) -> None:
        self.validate_coordinate(cell)

        self._cell_values[cell.y][cell.x] = value

    def get_parent(self, child: Cell) -> Cell | None:
        return self._parents[child.y][child.x]

    def set_parent(self, child: Cell, parent: Cell) -> None:
        self._parents[child.y][child.x] = parent

    def get_neighbor_cell(
        self,
        cell: Cell,
        direction: Direction,
    ) -> Cell | None:
        self.validate_coordinate(cell)

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

    def _get_neighbor_cells(self, cell: Cell) -> list[Cell]:
        return [
            neighbor
            for neighbor in (
                self.get_neighbor_cell(cell, direction)
                for direction in Direction
            )
            if neighbor is not None
        ]

    def get_reachable_neighbors(self, cell: Cell) -> list[Cell]:
        return [
            neighbor
            for neighbor in self._get_neighbor_cells(cell)
            if self.get_wall_state(
                cell,
                cell.get_direction_to_neighbor(neighbor),
            )
            is WallState.OPEN
        ]

    def get_unmarked_neighbors(self, cell: Cell) -> list[Cell]:
        return [
            neighbor
            for neighbor in self._get_neighbor_cells(cell)
            if self.get_cell_marking(neighbor) == CellMarking.UNMARKED
        ]

    def get_reachable_unmarked_neighbors(self, cell: Cell) -> list[Cell]:
        return [
            neighbor
            for neighbor in self.get_reachable_neighbors(cell)
            if self.get_cell_marking(neighbor) == CellMarking.UNMARKED
        ]

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

    def _set_wall_state(
        self,
        cell: Cell,
        direction: Direction,
        state: WallState,
    ) -> None:
        self.validate_coordinate(cell)

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
        self.validate_coordinate(cell)

        north = self.get_wall_state(cell, Direction.NORTH)
        east = self.get_wall_state(cell, Direction.EAST)
        south = self.get_wall_state(cell, Direction.SOUTH)
        west = self.get_wall_state(cell, Direction.WEST)

        return CellState(north, east, south, west)

    def _get_all_cell_states(self) -> list[list[CellState]]:
        return [
            [self._get_cell_state(Cell(x, y)) for x in range(self.width)]
            for y in range(self.height)
        ]

    def into_file_format(self) -> str:
        return (
            "\n".join([
                "".join([cell.to_hex() for cell in cell_list])
                for cell_list in self._get_all_cell_states()
            ])
            + "\n"
        )

    def get_collect_closed_walls(self) -> list:
        closed_walls = [
            (Cell(x, y), Direction.SOUTH)
            for x in range(self.width)
            for y in range(self.height)
            if y < self.height - 1
            and self.get_wall_state(Cell(x, y), Direction.SOUTH)
            == WallState.CLOSED
            and self.get_cell_value(Cell(x, y + 1)) != CellValue.FORTY_TWO
            and self.get_cell_value(Cell(x, y)) != CellValue.FORTY_TWO
        ]
        closed_walls = [
            (Cell(x, y), Direction.WEST)
            for x in range(self.width)
            for y in range(self.height)
            if x > 0
            and self.get_wall_state(Cell(x, y), Direction.WEST)
            == WallState.CLOSED
            and self.get_cell_value(Cell(x - 1, y)) != CellValue.FORTY_TWO
            and self.get_cell_value(Cell(x, y)) != CellValue.FORTY_TWO
        ]
        return closed_walls
