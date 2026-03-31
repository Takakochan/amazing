from mazegen.generators.base import Generator
from mazegen.generators.dfs import GeneratorDFS
from mazegen.grid import Grid


class GeneratorBasic(Generator):
    @staticmethod
    def generate(grid: Grid) -> None:
        GeneratorDFS.generate(grid)
