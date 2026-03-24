from dataclasses import dataclass
from typing import Self

from mazegen.direction import Direction


class CellError(Exception):
    pass


@dataclass
class Cell:
    x: int
    y: int

    def validate(
        self,
        width: int,
        height: int,
    ) -> None:
        if self.x < 0 or self.x >= width:
            raise CellError(f"x coordinate is out of range: `{self.x}`")

        if self.y < 0 or self.y >= height:
            raise CellError(f"y coordinate is out of range: `{self.y}`")

    def is_in_range(
        self,
        width: int,
        height: int,
    ) -> bool:
        return (
            self.x >= 0 and self.x < width and self.y >= 0 and self.y < height
        )

    def is_at_edge(
        self,
        width: int,
        height: int,
    ) -> bool:
        return (
            self.x == 0
            or self.x == width - 1
            or self.y == 0
            or self.y == height - 1
        )

    def is_neighbor_of(self, neighbor: Self) -> bool:
        dx = self.x - neighbor.x
        dy = self.y - neighbor.y

        return abs(dx) + abs(dy) == 1

    def get_direction_to_neighbor(self, neighbor: Self) -> Direction:
        dx = self.x - neighbor.x
        dy = self.y - neighbor.y

        match (dx, dy):
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

    def into_file_format(self) -> str:
        return f"{self.x},{self.y}\n"
