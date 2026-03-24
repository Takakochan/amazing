from mazegen.direction import Direction
from mazegen.grid import Grid


class MazeGenerator(Grid):
    def generate(
        self,
        entry: tuple[int, int],
        exit: tuple[int, int],  # noqa: A002
        perfect: bool,  # noqa: FBT001
    ) -> None:
        self._entry = entry
        self._exit = exit

        stack = []

        entry_cell = self.get_cell(entry[0], entry[1])

        self.mark_cell(entry_cell.x, entry_cell.y)
        stack.append(entry_cell)

        while len(stack) != 0:
            current_cell = stack.pop()
            neighbors = self.get_cell_unmarked_neighbors(
                current_cell.x,
                current_cell.y,
            )
            if len(neighbors) == 0:
                continue

            stack.append(current_cell)

            neighbor = neighbors[0]

            dx = current_cell.x - neighbor.x
            dy = current_cell.y - neighbor.y

            match (dx, dy):
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

            self.open_wall(current_cell.x, current_cell.y, direction)

            self.mark_cell(neighbor.x, neighbor.y)
            stack.append(neighbor)

            print()
            self.display()

        self.init_cells()

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
