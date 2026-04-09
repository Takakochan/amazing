from abc import ABC, abstractmethod

from mazegen.grid import Grid
from mazegen.render.base import Renderer


class Generator(ABC):
    @abstractmethod
    def generate(
        self,
        grid: Grid,
        seed: int | None,
        renderer: Renderer,
        animation: bool,
    ) -> int:
        pass
