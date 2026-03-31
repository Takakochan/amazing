from abc import ABC, abstractmethod

from mazegen.animation import GridDisplayer


class Generator(ABC):
    @abstractmethod
    def generate(self, grid: GridDisplayer) -> None:
        pass
