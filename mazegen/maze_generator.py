import sys
from typing import TYPE_CHECKING, Literal

from mazegen.cell import Cell
from mazegen.cell_value import CellValue
from mazegen.generators.basic import GeneratorBasic
from mazegen.generators.imperfect import GeneratorImperfect
from mazegen.generators.dfs import GeneratorDFS
from mazegen.grid import FortyTwoPatternError, Grid
from mazegen.render.ascii_renderer import AsciiRenderer
from mazegen.solvers.a_star import SolverAStar
from mazegen.solvers.bfs import SolverBFS
from mazegen.solvers.dfs import SolverDFS

if TYPE_CHECKING:
    from mazegen.solvers.base import Solver


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],  # noqa: A002
        animation_speed: int,
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

        self.renderer = AsciiRenderer(animation_speed)

    def display(self) -> None:
        self.renderer.display_grid(self.grid)

    def generate(
        self,
        perfect: bool,
        seed: int | None,
        animation: bool,
    ) -> None:
        generator = GeneratorDFS() if perfect else GeneratorImperfect()

        self.seed = generator.generate(
            self.grid,
            seed,
            self.renderer,
            animation,
        )

    def solve(
        self,
        algorithm: Literal["DFS", "BFS", "A*"] | None,
        animation: bool,
    ) -> None:
        solver: Solver = SolverBFS()

        match algorithm:
            case "DFS":
                solver = SolverDFS()
            case "BFS":
                solver = SolverBFS()
            case "A*":
                solver = SolverAStar()

        self.solution = solver.solve(
            self.grid,
            self.entry,
            self.exit,
            self.renderer,
            animation,
        )

    def save(self, filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(self.grid.into_file_format())
            file.write("\n")
            file.write(self.entry.into_file_format())
            file.write(self.exit.into_file_format())
            file.write(
                "".join([
                    direction.into_file_format() for direction in self.solution
                ])
                + "\n",
            )
