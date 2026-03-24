import random
import sys

from mazegen.cell import Cell
from mazegen.grid import FortyTwoPatternError, Grid


def generate_dfs(
    width: int,
    height: int,
    entry: Cell,
    exit: Cell,  # noqa: A002
) -> Grid:
    grid = Grid(width, height)

    try:
        grid.set_forty_two_pattern([entry, exit])
    except FortyTwoPatternError as error:
        print(
            f"\033[91mcould not draw 42 pattern: {error}\033[0m",
            file=sys.stderr,
        )

    stack: list[Cell] = []

    cell = Cell(0, 0)
    grid.mark_cell(cell)
    stack.append(cell)

    while stack:
        current = stack[-1]

        neighbors = grid.get_unmarked_neighbors(current)
        if not neighbors:
            stack.pop()
            continue

        neighbor = random.choice(neighbors)

        try:
            direction = current.get_direction_to_neighbor(neighbor)
        except RuntimeError as error:
            raise error

        grid.open_wall(current, direction)
        grid.mark_cell(neighbor)
        stack.append(neighbor)

    grid.unmark_cells()

    return grid


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],  # noqa: A002
    ) -> None:
        self.width = width
        self.height = height
        self.entry = Cell(entry[0], entry[1])
        self.exit = Cell(exit[0], exit[1])

    def generate(
        self,
        perfect: bool,  # noqa: FBT001
        seed: int | None = None,
    ) -> None:
        random.seed(seed)

        if perfect:
            self.grid = generate_dfs(
                self.width,
                self.height,
                self.entry,
                self.exit,
            )
        else:
            self.grid = generate_dfs(
                self.width,
                self.height,
                self.entry,
                self.exit,
            )

    def solve(self) -> None:
        self._solution = None

    def display(self) -> None:
        self.grid.display()

    def save(self, filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(self.grid.into_file_format())
            file.write("\n")
            file.write(self.entry.into_file_format())
            file.write(self.exit.into_file_format())

            # TODO: write solution to output file
            file.write("<solution>\n")
