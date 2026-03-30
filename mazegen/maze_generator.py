import random
import sys

from mazegen.cell import Cell
from mazegen.cell_value import CellValue
from mazegen.generators.basic import GeneratorBasic
from mazegen.generators.dfs import GeneratorDFS
from mazegen.grid import FortyTwoPatternError, Grid
from mazegen.solvers.bfs import SolverBFS
from mazegen.solvers.a_star import SolverAstar


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],  # noqa: A002
    ) -> None:
        self.entry = Cell(entry[0], entry[1])
        self.exit = Cell(exit[0], exit[1])

        self.grid = Grid(width, height)
        self.grid.set_cell_value(self.entry, CellValue.ENTRY)
        self.grid.set_cell_value(self.exit, CellValue.EXIT)

        try:
            self.grid.set_forty_two_pattern([self.entry, self.exit])
        except FortyTwoPatternError as error:
            print(
                f"\033[91mcould not draw 42 pattern: {error}\033[0m",
                file=sys.stderr,
            )

    def generate(
        self,
        perfect: bool,  # noqa: FBT001
        seed: int | None = None,
    ) -> None:
        random.seed(seed)

        generator = GeneratorDFS if perfect else GeneratorBasic
        generator.generate(self.grid)

        self.grid.display()

    def solve(self) -> None:
        solver = SolverAstar()
        solver.solve(self.grid, self.entry, self.exit)

        self.grid.display()

    def save(self, filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(self.grid.into_file_format())
            file.write("\n")
            file.write(self.entry.into_file_format())
            file.write(self.exit.into_file_format())

            # TODO: write solution to output file
            file.write("<solution>\n")

    def display(self) -> None:
        self.grid.display()
