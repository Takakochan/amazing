from dataclasses import dataclass

from mazegen.cell import Cell
from mazegen.cell_state import CellState
from mazegen.cell_value import CellValue
from mazegen.direction import Direction
from mazegen.wall_state import WallState


@dataclass
class Grid:
    width: int
    height: int

    def __post_init__(self) -> None:
        self.init_cells()
        self.init_walls()

    def _validate_coordinate(
        self,
        cell: Cell,
    ) -> None:
        cell.validate(self.width, self.height)

    def init_cells(self) -> None:
        self._cells = [
            [CellValue.UNMARKED for _x in range(self.width)]
            for _y in range(self.height)
        ]

    def init_walls(self) -> None:
        self._north_walls = [
            [WallState.CLOSED for _x in range(self.width)]
            for _y in range(self.height + 1)
        ]

        self._west_walls = [
            [WallState.CLOSED for _x in range(self.width + 1)]
            for _y in range(self.height)
        ]

    def _get_cell_value(self, cell: Cell) -> CellValue:
        self._validate_coordinate(cell)

        return self._cells[cell.y][cell.x]

    def _set_cell_value(self, cell: Cell, value: CellValue) -> None:
        self._validate_coordinate(cell)

        self._cells[cell.y][cell.x] = value

    def unmark_cell(self, cell: Cell) -> None:
        self._validate_coordinate(cell)

        self._set_cell_value(cell, CellValue.UNMARKED)

    def mark_cell(self, cell: Cell) -> None:
        self._validate_coordinate(cell)

        self._set_cell_value(cell, CellValue.MARKED)

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

    def _print_cell_value(self, cell: Cell) -> None:
        value = self._get_cell_value(cell)
        print(f" {value} ", end="")

    def _print_wall(self, cell: Cell, direction: Direction) -> None:
        self._validate_coordinate(cell)

        match (self._get_wall_state(cell, direction), direction):
            case (WallState.OPEN, Direction.NORTH | Direction.SOUTH):
                print("   ", end="")
            case (WallState.OPEN, Direction.WEST | Direction.EAST):
                print(" ", end="")
            case (WallState.CLOSED, Direction.NORTH | Direction.SOUTH):
                print("---", end="")
            case (WallState.CLOSED, Direction.WEST | Direction.EAST):
                print("|", end="")

    def display(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                print("+", end="")
                self._print_wall(Cell(x, y), Direction.NORTH)

            print("+", end="")
            print()

            for x in range(self.width):
                self._print_wall(Cell(x, y), Direction.WEST)
                self._print_cell_value(Cell(x, y))

            self._print_wall(Cell(self.width - 1, y), Direction.EAST)
            print()

        for x in range(self.width):
            print("+", end="")
            self._print_wall(
                Cell(x, self.height - 1),
                Direction.SOUTH,
            )

        print("+", end="")
        print()
