from dataclasses import dataclass

from mazegen.cell import Cell
from mazegen.cell_state import CellState
from mazegen.cell_value import CellValue
from mazegen.direction import Direction
from mazegen.wall_state import WallState


class CoordinateError(Exception):
    pass


@dataclass
class Grid:
    width: int
    height: int

    def __post_init__(self) -> None:
        self.init_cells()
        self.init_walls()

    def _validate_coordinates(
        self,
        x: int,
        y: int,
    ) -> None:
        if x < 0 or x >= self.width:
            raise CoordinateError(f"coordinate `{x}` is out of range")

        if y < 0 or y >= self.height:
            raise CoordinateError(f"coordinate `{y}` is out of range")

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

    def get_cell_value(self, x: int, y: int) -> CellValue:
        self._validate_coordinates(x, y)

        return self._cells[y][x]

    def _set_cell_value(self, x: int, y: int, value: CellValue) -> None:
        self._validate_coordinates(x, y)

        self._cells[y][x] = value

    def unmark_cell(self, x: int, y: int) -> None:
        self._set_cell_value(x, y, CellValue.UNMARKED)

    def mark_cell(self, x: int, y: int) -> None:
        self._set_cell_value(x, y, CellValue.MARKED)

    def get_cell(self, x: int, y: int) -> Cell:
        self._validate_coordinates(x, y)

        return Cell(x, y, self.get_cell_value(x, y))

    def get_cell_neighbor(
        self,
        x: int,
        y: int,
        direction: Direction,
    ) -> Cell | None:
        self._validate_coordinates(x, y)

        match direction:
            case Direction.NORTH:
                if y == 0:
                    return None
                return self.get_cell(x, y - 1)
            case Direction.EAST:
                if x == self.width - 1:
                    return None
                return self.get_cell(x + 1, y)
            case Direction.SOUTH:
                if y == self.height - 1:
                    return None
                return self.get_cell(x, y + 1)
            case Direction.WEST:
                if x == 0:
                    return None
                return self.get_cell(x - 1, y)

    def get_cell_neighbors(
        self,
        x: int,
        y: int,
    ) -> list[Cell]:
        return [
            cell
            for cell in (
                self.get_cell_neighbor(x, y, direction)
                for direction in Direction
            )
            if cell is not None
        ]

    def get_cell_unmarked_neighbors(
        self,
        x: int,
        y: int,
    ) -> list[Cell]:
        return [
            cell
            for cell in self.get_cell_neighbors(x, y)
            if cell.value == CellValue.UNMARKED
        ]

    def get_wall_state(
        self,
        x: int,
        y: int,
        direction: Direction,
    ) -> WallState:
        self._validate_coordinates(x, y)

        match direction:
            case Direction.NORTH:
                return self._north_walls[y][x]
            case Direction.EAST:
                return self._west_walls[y][x + 1]
            case Direction.SOUTH:
                return self._north_walls[y + 1][x]
            case Direction.WEST:
                return self._west_walls[y][x]

    def get_cell_state(self, x: int, y: int) -> CellState:
        self._validate_coordinates(x, y)

        north = self.get_wall_state(x, y, Direction.NORTH)
        east = self.get_wall_state(x, y, Direction.EAST)
        south = self.get_wall_state(x, y, Direction.SOUTH)
        west = self.get_wall_state(x, y, Direction.WEST)

        return CellState(north, east, south, west)

    def get_cell_state_grid(self) -> list[list[CellState]]:
        return [
            [self.get_cell_state(x, y) for x in range(self.width)]
            for y in range(self.height)
        ]

    def _set_wall_state(
        self,
        x: int,
        y: int,
        direction: Direction,
        state: WallState,
    ) -> None:
        self._validate_coordinates(x, y)

        match direction:
            case Direction.NORTH:
                self._north_walls[y][x] = state
            case Direction.EAST:
                self._west_walls[y][x + 1] = state
            case Direction.SOUTH:
                self._north_walls[y + 1][x] = state
            case Direction.WEST:
                self._west_walls[y][x] = state

    def open_wall(self, x: int, y: int, direction: Direction) -> None:
        self._set_wall_state(x, y, direction, WallState.OPEN)

    def close_wall(self, x: int, y: int, direction: Direction) -> None:
        self._set_wall_state(x, y, direction, WallState.CLOSED)

    def _print_cell_value(self, x: int, y: int) -> None:
        value = self.get_cell_value(x, y)
        print(f" {value} ", end="")

    def _print_wall(self, x: int, y: int, direction: Direction) -> None:
        self._validate_coordinates(x, y)

        # match self.get_wall_state(x, y, direction):
        #     case WallState.OPEN:
        #         print(" ", end="")
        #     case WallState.CLOSED:
        #         match direction:
        #             case Direction.NORTH | Direction.SOUTH:
        #                 print("---", end="")
        #             case Direction.WEST | Direction.EAST:
        #                 print("|", end="")

        match (self.get_wall_state(x, y, direction), direction):
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
                self._print_wall(x, y, Direction.NORTH)

            print("+", end="")
            print()

            for x in range(self.width):
                self._print_wall(x, y, Direction.WEST)
                self._print_cell_value(x, y)

            self._print_wall(self.width - 1, y, Direction.EAST)
            print()

        for x in range(self.width):
            print("+", end="")
            self._print_wall(x, self.height - 1, Direction.SOUTH)

        print("+", end="")
        print()
