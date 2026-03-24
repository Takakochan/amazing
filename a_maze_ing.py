"""The main A-Maze-ing program."""

import sys

from config import Config, ConfigError
from mazegen import MazeGenerator


def main() -> None:
    try:
        config = Config.from_file(sys.argv[1])
    except ConfigError as error:
        raise error

    maze_generator = MazeGenerator(config.width, config.height)
    maze_generator.generate(
        config.entry,
        config.exit,
        config.perfect,
    )
    maze_generator.solve()
    maze_generator.save(config.output_file)


if __name__ == "__main__":
    main()
