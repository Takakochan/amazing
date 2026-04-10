from abc import abstractmethod

import random

from mazegen.cell import Cell
from mazegen.direction import Direction
from mazegen.generators.base import Generator
from mazegen.generators.dfs import GeneratorDFS
from mazegen.grid import Grid
from mazegen.render.base import Renderer
from mazegen.wall_state import WallState


class GeneratorImperfect(Generator):
	def generate(
		self,
		grid: Grid,
		seed: int | None,
		renderer: Renderer,
		animation: bool
	) -> int:
		generator = GeneratorDFS()
		generator.generate(grid, seed, renderer, animation)
		closed_walls = self._collect_closed_walls(grid)
		self._open_random_walls(grid, renderer, closed_walls)
		return GeneratorDFS().generate(grid, seed, renderer, animation)

	def _collect_closed_walls(self, grid: Grid) -> list:
		closed_walls = []
		for x in range(grid.width):
			for y in range(grid.height):
				cell = Cell(x, y)
				if y < grid.height - 1 and grid.get_wall_state(cell, Direction.SOUTH) == WallState.CLOSED:
					closed_walls.append((cell, Direction.SOUTH))
				if x > 0 and grid.get_wall_state(cell, Direction.WEST) == WallState.CLOSED:
					closed_walls.append((cell, Direction.WEST))
		return closed_walls

	def _open_random_walls(
			self,
			grid: Grid,
			renderer: Renderer,
			closed_walls: list,
			ratio: float = 0.0,
	) -> None:
		count = max(1, int(len(closed_walls) * ratio))
		chosen = random.sample(closed_walls, min(count, len(closed_walls)))
		for cell, direction in chosen:
			grid.open_wall(cell, direction)
			renderer.display_cell(grid, cell)
