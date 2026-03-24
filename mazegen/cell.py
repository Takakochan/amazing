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

    def into_file_format(self) -> str:
        return f"{self.x},{self.y}\n"
