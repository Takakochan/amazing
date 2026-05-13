from src.mazegen import MazeGenerator


def main() -> None:
    maze_generator = MazeGenerator(
        src=(0, 0),
        dest=(19, 19),
        width=20,
        height=20,
    )
    maze_generator.generate(perfect=True, seed=None)
    maze_generator.solve("A*")
    print(maze_generator.solution)
    print(maze_generator.into_file_format())


if __name__ == "__main__":
    main()
