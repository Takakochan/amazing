import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, Self

from src.config import Config
from src.mazegen.cell import Cell
from src.mazegen.cell_value import CellValue
from src.mazegen.direction import Direction
from src.mazegen.generators.dfs import GeneratorDFS
from src.mazegen.generators.imperfect import GeneratorImperfect
from src.mazegen.grid import FortyTwoPatternError, Grid
from src.mazegen.render.ascii_renderer import AsciiRenderer
from src.mazegen.render.base import Renderer
from src.mazegen.solvers.a_star import SolverAStar
from src.mazegen.solvers.bfs import SolverBFS
from src.mazegen.solvers.dfs import SolverDFS

if TYPE_CHECKING:
    from src.mazegen.solvers.base import Solver


def validate(
    src: tuple[int, int],
    dest: tuple[int, int],
    width: int,
    height: int,
) -> None:
    if src == dest:
        raise ValueError(
            f"src and dest must be different: `{src}`",
        )

    if width <= 0:
        raise ValueError(f"width must be positive: `{width}`")

    if height <= 0:
        raise ValueError(f"height must be positive: `{height}`")

    if src[0] < 0 or src[0] >= width or src[1] < 0 or src[1] >= height:
        raise ValueError(f"src must be in grid range: `{src}`")

    if dest[0] < 0 or dest[0] >= width or dest[1] < 0 or dest[1] >= height:
        raise ValueError(f"dest must be in grid range: `{dest}`")


@dataclass
class MazeGenerator:
    """Generate and solve a maze.

    Attributes:
        src: the starting coordinates
        dest: the ending coordinates
        width: the width of the maze
        height: the height of the maze
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
        validate(src, dest, width, height)

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
