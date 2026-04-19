from config import Config
from mazegen import MazeGenerator
from mazegen.wall_state import WallState

CONFIG = Config(
    18,
    18,
    (0, 0),
    (17, 17),
    "/tmp/test_maze_",
    True,
)


def run(config: Config, seed: int) -> None:
    maze_generator = MazeGenerator.from_config(config)

    maze_generator.generate(config.perfect, seed)

    closed = maze_generator.grid.get_collect_closed_walls()

    for cell, direction in closed:
        assert (
            maze_generator.grid.get_wall_state(cell, direction)
            == WallState.CLOSED
        ), f"The wall of cell {cell} in direction {direction} should be closed"


def test_solver_range_0_50() -> None:
    for seed in range(0, 50):
        run(CONFIG, seed)


def test_solver_range_50_100() -> None:
    for seed in range(50, 100):
        run(CONFIG, seed)


def test_solver_range_100_150() -> None:
    for seed in range(100, 150):
        run(CONFIG, seed)


def test_solver_range_150_200() -> None:
    for seed in range(100, 150):
        run(CONFIG, seed)
