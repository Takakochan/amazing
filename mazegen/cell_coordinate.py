from dataclasses import dataclass
from typing import Self

from mazegen.direction import Direction


class CoordinateError(Exception):
    pass


@dataclass
class CellCoordinate:
    x: int
    y: int

    def get_direction_to_neighbor(self, neighbor: Self) -> Direction:
        match (
            self.x - neighbor.x,
            self.y - neighbor.y,
        ):
            case (0, 1):
                return Direction.NORTH
            case (0, -1):
                return Direction.SOUTH
            case (1, 0):
                return Direction.WEST
            case (-1, 0):
                return Direction.EAST
            case _:
                raise RuntimeError(
                    f"`{neighbor}` is not a neighbor of `{self}`",
                )
