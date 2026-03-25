"""The main A-Maze-ing program."""

import sys

from config import Config, ConfigError
from mazegen import MazeGenerator


def main() -> None:
    try:
        config = Config.from_file(sys.argv[1])
    except ConfigError as error:
        raise error

    maze_generator = MazeGenerator(
        config.width,
        config.height,
        config.entry,
        config.exit,
    )

    maze_generator.generate(config.perfect, config.seed)
    maze_generator.solve()
    maze_generator.save(config.output_file)


if __name__ == "__main__":
    main()
