from mazegen.generators.base import Generator
from mazegen.generators.dfs import GeneratorDFS
from mazegen.grid import Grid


class GeneratorBasic(Generator):
    def generate(grid: Grid) -> None:
        GeneratorDFS.generate(grid)
