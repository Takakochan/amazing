"""The main A-Maze-ing program."""

import sys

from maze import Maze


def main() -> None:
    maze = Maze.from_config_file(sys.argv[1])
    maze.display()


if __name__ == "__main__":
    main()
