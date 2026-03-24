import random

from mazegen.cell import Cell
from mazegen.direction import Direction
from mazegen.grid import Grid


def generate_dfs(grid: Grid, entry: Cell) -> None:
    grid.init_cells()
    grid.init_walls()

    stack = []

    entry_cell = grid.get_cell(entry.x, entry.y)
    grid.mark_cell(entry_cell.x, entry_cell.y)
    stack.append(entry_cell)

    while len(stack) != 0:
        current_cell = stack.pop()
        neighbors = grid.get_cell_unmarked_neighbors(
            current_cell.x,
            current_cell.y,
        )
        if len(neighbors) == 0:
            continue

        stack.append(current_cell)

        neighbor_cell = random.choice(neighbors)

        match (
            current_cell.x - neighbor_cell.x,
            current_cell.y - neighbor_cell.y,
        ):
            case (0, 1):
                direction = Direction.NORTH
            case (0, -1):
                direction = Direction.SOUTH
            case (1, 0):
                direction = Direction.WEST
            case (-1, 0):
                direction = Direction.EAST
            case _:
                raise RuntimeError("neighbor is not a neighbor")

        grid.open_wall(current_cell.x, current_cell.y, direction)
        grid.mark_cell(neighbor_cell.x, neighbor_cell.y)
        stack.append(neighbor_cell)

    grid.init_cells()


class MazeGenerator(Grid):
    def generate(
        self,
        entry: tuple[int, int],
        exit: tuple[int, int],  # noqa: A002
        perfect: bool,  # noqa: FBT001
        seed: int | None = None,
    ) -> None:
        self._entry = entry
        self._exit = exit

        random.seed(seed)
        generate_dfs(self, self.get_cell(entry[0], entry[1]))

    def solve(
        self,
    ) -> None:
        self._solution = None
        self.init_cells()

    def save(self, filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as file:
            for cell_list in self.get_cell_state_grid():
                for cell in cell_list:
                    file.write(cell.to_hex())
                file.write("\n")
            file.write("\n")

            file.write(f"{self._entry[0]},{self._entry[1]}\n")
            file.write(f"{self._exit[0]},{self._exit[1]}\n")

            # TODO: write solution to output file
            file.write("<solution>\n")
