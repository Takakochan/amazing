import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, Self

from config import Config
from mazegen.cell import Cell
from mazegen.cell_value import CellValue
from mazegen.generators.dfs import GeneratorDFS
from mazegen.generators.imperfect import GeneratorImperfect
from mazegen.grid import FortyTwoPatternError, Grid
from mazegen.render.ascii_renderer import AsciiRenderer
from mazegen.render.base import Renderer
from mazegen.solvers.a_star import SolverAStar
from mazegen.solvers.bfs import SolverBFS
from mazegen.solvers.dfs import SolverDFS

if TYPE_CHECKING:
    from mazegen.solvers.base import Solver


@dataclass
class MazeGenerator:
    src: Cell
    dest: Cell
    grid: Grid
    renderer: Renderer

    @classmethod
    def from_config(cls, config: Config) -> Self:
        src = Cell(config.entry[0], config.entry[1])
        dest = Cell(config.exit[0], config.exit[1])

        grid = Grid(config.width, config.height)
        grid.set_cell_value(src, CellValue.ENTRY)
        grid.set_cell_value(dest, CellValue.EXIT)

        try:
            grid.set_forty_two_pattern([src, dest])
        except FortyTwoPatternError as error:
            print(
                f"\033[91mcould not draw 42 pattern: {error}\033[0m",
                file=sys.stderr,
            )

        renderer = AsciiRenderer.from_config(config)

        return cls(src, dest, grid, renderer)

    def display(self) -> None:
        self.renderer.display_grid(self.grid)

    def generate(
        self,
        perfect: bool,
        seed: int | None,
    ) -> None:
        generator = GeneratorDFS() if perfect else GeneratorImperfect()

        self.seed = generator.generate(self.grid, seed, self.renderer)

    def solve(self, algorithm: Literal["DFS", "BFS", "A*"] | None) -> None:
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
            self.src,
            self.dest,
            self.renderer,
        )

    def save(self, filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(self.grid.into_file_format())
            file.write("\n")
            file.write(self.src.into_file_format())
            file.write(self.dest.into_file_format())
            file.write(
                "".join([
                    direction.into_file_format() for direction in self.solution
                ])
                + "\n",
            )
