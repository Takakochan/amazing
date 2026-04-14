from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from typing import Self

from config import Config
from mazegen import MazeGenerator


class Event(StrEnum):
    GENERATE = "g"
    SHOW_SOLUTION = "s"
    HIDE_SOLUTION = "h"
    SAVE = "S"
    QUIT = "q"


@dataclass
class State(ABC):
    maze_generator: MazeGenerator
    config: Config

    @abstractmethod
    def on_event(self, event: Event) -> Self:
        pass


class GenerateState(State):
    @classmethod
    def from_config(cls, config: Config) -> Self:
        maze_generator = MazeGenerator.from_config(config)

        if config.animation:
            maze_generator.display()

        maze_generator.generate(config.perfect, config.seed)
        maze_generator.display()

        print(f"Generated maze (seed: {maze_generator.seed})")
        print()
        print("[g]enerate | [s]olve | [q]uit")

        return cls(maze_generator, config)

    def on_event(self, event: Event) -> State:
        match event:
            case Event.GENERATE:
                return GenerateState.from_config(self.config)
            case Event.SHOW_SOLUTION:
                return SolveState.from_generated(self)
            case Event.HIDE_SOLUTION:
                return self
            case Event.SAVE:
                return self
            case Event.QUIT:
                return self


class SolveState(State):
    @classmethod
    def from_generated(cls, generated: GenerateState) -> Self:
        generated.maze_generator.solve(generated.config.algorithm)
        generated.maze_generator.display()

        print(f"Solved maze (seed: {generated.maze_generator.seed})")
        print()
        print("[g]enerate | [h]ide solution | [S]ave | [q]uit")

        return cls(generated.maze_generator, generated.config)

    def on_event(self, event: Event) -> State:
        match event:
            case Event.GENERATE:
                return GenerateState.from_config(self.config)
            case Event.SHOW_SOLUTION:
                if not self.maze_generator.renderer.show_solution():
                    return self

                self.maze_generator.display()

                print(f"Solved maze (seed: {self.maze_generator.seed})")
                print()
                print("[g]enerate | [h]ide solution | [S]ave | [q]uit")
                return self
            case Event.HIDE_SOLUTION:
                if not self.maze_generator.renderer.hide_solution():
                    return self

                self.maze_generator.display()

                print(f"Solved maze (seed: {self.maze_generator.seed})")
                print()
                print("[g]enerate | [s]how solution | [S]ave | [q]uit")
                return self
            case Event.SAVE:
                return SaveState.from_solved(self)
            case Event.QUIT:
                return self


class SaveState(State):
    @classmethod
    def from_solved(cls, solved: SolveState) -> Self:
        solved.maze_generator.save(solved.config.output_file)
        solved.maze_generator.display()

        print(f"Saved maze to `{solved.config.output_file}`")
        print()
        print("[g]enerate | [q]uit")

        return cls(solved.maze_generator, solved.config)

    def on_event(self, event: Event) -> State:
        match event:
            case Event.GENERATE:
                return GenerateState.from_config(self.config)
            case Event.SHOW_SOLUTION:
                return self
            case Event.HIDE_SOLUTION:
                return self
            case Event.SAVE:
                return self
            case Event.QUIT:
                return self
