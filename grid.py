from cell_state import CellState
from direction import Direction
from wall_state import WallState


class Grid:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        self._north_walls = [
            [WallState.closed for _x in range(width)]
            for _y in range(height + 1)
        ]

        self._west_walls = [
            [WallState.closed for _x in range(width + 1)]
            for _y in range(height)
        ]

    # TODO: validate x, y within range
    def cordinate_validate(
            self,
            x: int,
            y: int
    ) -> None:
        if 0 >= x > self.width:
            raise ValueError(f"cordinat {x} is out of range")
        if 0 >= x > self.width:
            raise ValueError(f"cordinat {x} is out of range")     
        

    def get_cell_wall_state(
        self,
        x: int,
        y: int,
        direction: Direction,
    ) -> WallState:
        match direction:
            case Direction.north:
                return self._north_walls[y][x]
            case Direction.east:
                return self._west_walls[y][x + 1]
            case Direction.south:
                return self._north_walls[y + 1][x]
            case Direction.west:
                return self._west_walls[y][x]

    def get_cell_state(self, x: int, y: int) -> CellState:
        north = self.get_cell_wall_state(x, y, Direction.north)
        east = self.get_cell_wall_state(x, y, Direction.east)
        south = self.get_cell_wall_state(x, y, Direction.south)
        west = self.get_cell_wall_state(x, y, Direction.west)

        return CellState(north, east, south, west)

    def get_cell_state_grid(self) -> list[list[CellState]]:
        return [
            [self.get_cell_state(x, y) for x in range(self.width)]
            for y in range(self.height)
        ]

    # TODO: validate x, y within range
    def _set_cell_wall_state(
        self,
        x: int,
        y: int,
        direction: Direction,
        state: WallState,
    ) -> None:
        match direction:
            case Direction.north:
                self._north_walls[y][x] = state
            case Direction.east:
                self._west_walls[y][x + 1] = state
            case Direction.south:
                self._north_walls[y + 1][x] = state
            case Direction.west:
                self._west_walls[y][x] = state

    # TODO: validate x, y within range
    def open_cell(self, x: int, y: int, direction: Direction) -> None:
        self._set_cell_wall_state(x, y, direction, WallState.open)

    # TODO: validate x, y within range
    def close_cell(self, x: int, y: int, direction: Direction) -> None:
        self._set_cell_wall_state(x, y, direction, WallState.closed)

    def _print_cell_wall(self, x: int, y: int, direction: Direction) -> None:
        match self.get_cell_wall_state(x, y, direction):
            case WallState.open:
                print(" ", end="")
            case WallState.closed:
                match direction:
                    case Direction.north | Direction.south:
                        print("-", end="")
                    case Direction.west | Direction.east:
                        print("|", end="")

    def display(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                print("+", end="")
                self._print_cell_wall(x, y, Direction.north)

            print("+", end="")
            print()

            for x in range(self.width):
                self._print_cell_wall(x, y, Direction.west)
                print(" ", end="")

            self._print_cell_wall(self.width, y, Direction.west)
            print()

        for x in range(self.width):
            print("+", end="")
            self._print_cell_wall(x, self.height, Direction.north)

        print("+", end="")
        print()
