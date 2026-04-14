from typing import Literal

from config import Config
from mazegen import MazeGenerator


def solve(
    maze_generator: MazeGenerator,
    algorithm: Literal["DFS", "BFS", "A*"],
    output_file: str,
) -> list:
    maze_generator.solve(algorithm)
    solution_bfs = maze_generator.solution
    maze_generator.save(output_file + algorithm)
    return solution_bfs


def run(config: Config, seed: int) -> None:
    maze_generator = MazeGenerator.from_config(config)

    maze_generator.generate(config.perfect, seed)

    solution_bfs = solve(maze_generator, "BFS", config.output_file)
    solution_a_star = solve(maze_generator, "A*", config.output_file)

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


def test_solver() -> None:
    config = Config(
        18,
        18,
        (0, 0),
        (17, 17),
        "/tmp/test_maze_",
        False,
    )

    for seed in range(100):
        run(config, seed)

    run(config, 1776190330919183478)
