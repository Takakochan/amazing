from abc import ABC, abstractmethod

from mazegen.grid import Grid


class Generator(ABC):
    @abstractmethod
    def generate(grid: Grid) -> None:
        pass
