"""The main A-Maze-ing program."""

import sys

from config import ConfigError
from maze import Maze


def main() -> None:
    try:
        maze = Maze.from_config_file(sys.argv[1])
    except ConfigError as error:
        raise error

    maze.display()
    maze.save()


if __name__ == "__main__":
    main()
