import random

from mazegen.cell import Cell
from mazegen.grid import Grid


def generate_dfs(grid: Grid, entry: Cell) -> None:
    grid.init_cells()
    grid.init_walls()

    stack: list[Cell] = []

    grid.mark_cell(entry)
    stack.append(entry)

    while stack:
        current = stack.pop()

        neighbors = grid.get_unmarked_neighbors(current)
        if not neighbors:
            continue

        stack.append(current)

        neighbor = random.choice(neighbors)

        try:
            direction = current.get_direction_to_neighbor(neighbor)
        except RuntimeError as error:
            raise error

        grid.open_wall(current, direction)
        grid.mark_cell(neighbor)
        stack.append(neighbor)

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
        generate_dfs(self, Cell(entry[0], entry[1]))

    def solve(
        self,
    ) -> None:
        self._solution = None
        self.init_cells()

    def save(self, filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as file:
            for cell_list in self.get_all_cell_states():
                for cell in cell_list:
                    file.write(cell.to_hex())
                file.write("\n")
            file.write("\n")

            file.write(f"{self._entry[0]},{self._entry[1]}\n")
            file.write(f"{self._exit[0]},{self._exit[1]}\n")

            # TODO: write solution to output file
            file.write("<solution>\n")
