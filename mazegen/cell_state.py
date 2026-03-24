"""The cell state."""

from dataclasses import dataclass
from typing import Self

from mazegen.wall_state import WallState


@dataclass
class CellState:
    """
    The state of a cell in the maze.

    Attributes:
        north: the state of the north wall
        east: the state of the east wall
        south: the state of the south wall
        west: the state of the west wall

    """

    north: WallState
    east: WallState
    south: WallState
    west: WallState

    @classmethod
    def open(cls) -> Self:
        """
        Create cell state with all walls open.

        Returns:
            A open cell state.

        """
        return cls(
            WallState.open,
            WallState.open,
            WallState.open,
            WallState.open,
        )

    @classmethod
    def closed(cls) -> Self:
        """
        Create cell state with all walls closed.

        Returns:
            A closed cell state.

        """
        return cls(
            WallState.closed,
            WallState.closed,
            WallState.closed,
            WallState.closed,
        )

    @classmethod
    def from_4_bit_int(cls, bits: int) -> Self:
        """
        Create cell state from a 4-bit integer.

        Args:
            bits: the 4-bit integer.

        Returns:
            A cell state.

        """

        if bits < 0 or bits > 0b1111:
            raise ValueError("bits must be a 4-bit int")

        north = WallState(bits & 1)
        east = WallState((bits >> 1) & 1)
        south = WallState((bits >> 2) & 1)
        west = WallState((bits >> 3) & 1)

        return cls(north, east, south, west)

    @classmethod
    def from_hex(cls, character: str) -> Self:
        """
        Create cell state from a hexadecimal character.

        Args:
            character: the hexadecimal character

        Returns:
            A cell state.

        """

        if len(character) != 1:
            raise ValueError("input string must be a single character")

        try:
            bits = int(character, 16)
        except ValueError as error:
            raise ValueError(
                "character must be a hexadecimal integer",
            ) from error

        return cls.from_4_bit_int(bits)

    def to_4_bit_int(self) -> int:
        """
        Convert the cell state into a 4-bit integer.

        Returns:
            A 4-bit integer representing the cell state.

        """
        return (
            self.west.value * 8
            + self.south.value * 4
            + self.east.value * 2
            + self.north.value
        )

    def to_hex(self) -> str:
        """
        Convert the cell state into a hexadecimal character.

        Returns:
            A hexadecimal character representing the cell state.

        """
        return f"{self.to_4_bit_int():X}"
