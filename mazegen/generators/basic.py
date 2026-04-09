from mazegen.generators.base import Generator
from mazegen.generators.dfs import GeneratorDFS
from mazegen.grid import Grid
from mazegen.render.base import Renderer


class GeneratorBasic(Generator):
    def generate(
        self,
        grid: Grid,
        seed: int | None,
        renderer: Renderer,
        animation: bool,
    ) -> None:
        self._foo = None

        GeneratorDFS().generate(grid, seed, renderer, animation)
