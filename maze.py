"""The maze class."""

from dataclasses import dataclass

from cell_state import CellState


@dataclass
class Maze:
    """
    The maze.

    Attributes:
        width: the width of the maze.
        height: the height of the maze.
        entry: the (x, y) coordinates of the entry to the maze.
        exit: the (x, y) coordinates of the exit to the maze.
        output_file: the file to write the maze in.
        perfect: option to ensure exactly one path from entry to exit.

    """

    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool

    grid: list[list[CellState]]

    def initialize_grid(self) -> None:
        """Initialize the grid of the maze."""
        self.grid = [
            [CellState.closed() for _y in range(self.height)]
            for _x in range(self.width)
        ]

    def randomize_grid(self) -> None:
        """Randomize the grid of the maze."""
        pass
