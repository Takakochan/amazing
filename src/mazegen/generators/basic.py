from src.mazegen.generators.base import Generator
from src.mazegen.generators.dfs import GeneratorDFS
from src.mazegen.grid import Grid
from src.mazegen.render.base import Renderer


class GeneratorBasic(Generator):
    def generate(
        self,
        grid: Grid,
        seed: int | None,
        renderer: Renderer,
    ) -> int:
        self._foo = None

        return GeneratorDFS().generate(grid, seed, renderer)
