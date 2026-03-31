from abc import ABC, abstractmethod

from mazegen.grid import Grid


class Generator(ABC):
    @abstractmethod
    @staticmethod
    def generate(grid: Grid) -> None:
        pass
