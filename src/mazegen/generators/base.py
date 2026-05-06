from abc import ABC, abstractmethod

from src.mazegen.grid import Grid
from src.mazegen.render.base import Renderer


class Generator(ABC):
    @abstractmethod
    def generate(
        self,
        grid: Grid,
        seed: int | None,
        renderer: Renderer,
    ) -> int:
        pass
