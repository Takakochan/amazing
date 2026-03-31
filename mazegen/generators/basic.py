from mazegen.animation import GridDisplayer
from mazegen.generators.base import Generator
from mazegen.generators.dfs import GeneratorDFS


class GeneratorBasic(Generator):
    def generate(self, grid: GridDisplayer) -> None:
        self._foo = None

        GeneratorDFS().generate(grid)
