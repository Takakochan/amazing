from cell_state import Direction, WallState


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
