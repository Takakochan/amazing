from abc import ABC, abstractmethod

from mazegen.grid_animation import GridAnimation


class Generator(ABC):
    @abstractmethod
    def generate(self, grid: GridAnimation) -> None:
        pass
