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

    def solve(
        self,
    ) -> None:
        self._solution = None

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
