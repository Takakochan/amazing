from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self

from config import Config
from mazegen import MazeGenerator

# TODO: create Event enum


@dataclass
class State(ABC):
    maze_generator: MazeGenerator
    config: Config

    def display(self) -> None:
        self.maze_generator.display()

    @abstractmethod
    def on_event(self, event: str) -> Self:
        pass


class Generated(State):
    @classmethod
    def from_config(cls, config: Config) -> Self:
        maze_generator = MazeGenerator(
            config.width,
            config.height,
            config.entry,
            config.exit,
            config.animation_speed,
        )

        maze_generator.display()

        maze_generator.generate(
            config.perfect,
            config.seed,
            config.animation,
        )

        maze_generator.display()

        print(f"Generated maze (seed: {config.seed})")
        print()
        print("[g]enerate | [s]olve | [q]uit")

        return cls(maze_generator, config)

    def on_event(self, event: str) -> State:
        match event:
            case "g":
                return Generated.from_config(self.config)
            case "s":
                return Solved.from_generated(self)
            case _:
                return self


class Solved(State):
    @classmethod
    def from_generated(cls, generated: Generated) -> Self:
        generated.maze_generator.solve(
            generated.config.algorithm,
            generated.config.animation,
        )

        generated.maze_generator.display()

        print(f"Solved maze (seed: {generated.config.seed})")
        print()
        print("[g]enerate | [S]ave | [q]uit")

        return cls(generated.maze_generator, generated.config)

    def on_event(self, event: str) -> State:
        match event:
            case "g":
                return Generated.from_config(self.config)
            case "S":
                return Saved.from_solved(self)
            case _:
                return self


class Saved(State):
    @classmethod
    def from_solved(cls, solved: Solved) -> Self:
        solved.maze_generator.save(solved.config.output_file)

        print(f"Saved maze to `{solved.config.output_file}`")
        print()
        print("[g]enerate | [q]uit")

        return cls(solved.maze_generator, solved.config)

    def on_event(self, event: str) -> State:
        match event:
            case "g":
                return Generated.from_config(self.config)
            case _:
                return self
