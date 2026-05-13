from src.mazegen import MazeGenerator
from src.mazegen.wall_state import WallState


def run(seed: int) -> None:
    maze_generator = MazeGenerator((0, 0), (17, 17), 18, 18)

    maze_generator.generate(True, seed)

    closed = maze_generator.grid.get_closed_walls()

    for cell, direction in closed:
        assert (
            maze_generator.grid.get_wall_state(cell, direction)
            == WallState.CLOSED
        ), f"The wall of cell {cell} in direction {direction} should be closed"


def test_solver_range_0_50() -> None:
    for seed in range(0, 50):
        run(seed)


def test_solver_range_50_100() -> None:
    for seed in range(50, 100):
        run(seed)


def test_solver_range_100_150() -> None:
    for seed in range(100, 150):
        run(seed)


def test_solver_range_150_200() -> None:
    for seed in range(150, 200):
        run(seed)
