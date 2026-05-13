from typing import Literal

from src.mazegen import MazeGenerator
from src.mazegen.direction import Direction


def solve(
    maze_generator: MazeGenerator,
    algorithm: Literal["DFS", "BFS", "A*"],
    output_file: str,
) -> list[Direction]:
    maze_generator.solve(algorithm)
    solution_bfs = maze_generator.solution
    maze_generator.save(output_file + algorithm)
    return solution_bfs or []


def run(seed: int) -> None:
    maze_generator = MazeGenerator((0, 0), (17, 17), 18, 18)

    maze_generator.generate(True, seed)

    output_file = "/tmp/test_maze_"
    solution_bfs = solve(maze_generator, "BFS", output_file)
    solution_a_star = solve(maze_generator, "A*", output_file)

    solution_bfs_string = "".join([
        direction.into_file_format() for direction in solution_bfs
    ])
    solution_a_star_string = "".join([
        direction.into_file_format() for direction in solution_a_star
    ])
    assert len(solution_bfs_string) == len(solution_a_star_string), (
        "BFS and A* should find solution string of same length"
    )

    assert len(solution_bfs) == len(solution_a_star), (
        "BFS and A* should find solution of same length"
    )


def test_solver_seed() -> None:
    run(1776190330919183478)


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
    for seed in range(100, 150):
        run(seed)
