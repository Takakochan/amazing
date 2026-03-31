from mazegen.generators.base import Generator
from mazegen.generators.dfs import GeneratorDFS
from mazegen.grid_animation import GridAnimation


class GeneratorBasic(Generator):
    def generate(self, grid: GridAnimation) -> None:
        self._foo = None

        GeneratorDFS().generate(grid)
