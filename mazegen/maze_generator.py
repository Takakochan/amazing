import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, Self

from config import Config
from mazegen.cell import Cell
from mazegen.cell_value import CellValue
from mazegen.direction import Direction
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
    """[TODO:description]

    Attributes:
        src: [TODO:attribute]
        dest: [TODO:attribute]
        grid: [TODO:attribute]
        renderer: [TODO:attribute]
        seed: [TODO:attribute]
        solution: [TODO:attribute]
    """

    src: Cell
    dest: Cell
    grid: Grid
    renderer: Renderer
    seed: int | None
    solution: list[Direction] | None

    def __init__(
        self,
        src: tuple[int, int],
        dest: tuple[int, int],
        width: int,
        height: int,
    ) -> None:
        self.src = Cell(src[0], src[1])
        self.dest = Cell(dest[0], dest[1])

        self.grid = Grid(width, height)
        self.grid.set_cell_value(self.src, CellValue.ENTRY)
        self.grid.set_cell_value(self.dest, CellValue.EXIT)

        try:
            self.grid.set_forty_two_pattern([self.src, self.dest])
        except FortyTwoPatternError as error:
            # TODO: display 42 pattern error more clearly
            print(
                f"\033[91mcould not draw 42 pattern: {error}\033[0m",
                file=sys.stderr,
            )

        self.renderer = AsciiRenderer.default()
        self.seed = None
        self.solution = None

    @classmethod
    def from_config(cls, config: Config) -> Self:
        maze_generator = cls(
            config.entry,
            config.exit,
            config.width,
            config.height,
        )
        maze_generator.renderer = AsciiRenderer.from_config(config)

        return maze_generator

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

            if self.solution:
                file.write(
                    "".join([
                        direction.into_file_format()
                        for direction in self.solution
                    ])
                    + "\n",
                )
