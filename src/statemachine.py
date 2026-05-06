# TODO: move file to separate directory

from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum, StrEnum, auto

from src.config import Config
from src.mazegen import MazeGenerator

type Action[C] = Callable[[C], None]


class InvalidTransition(Exception):
    pass


@dataclass
class Context:
    maze_generator: MazeGenerator
    config: Config


class State(Enum):
    GENERATE = auto()
    SOLVE = auto()
    SAVE = auto()
    QUIT = auto()


class Event(StrEnum):
    GENERATE = "g"
    SHOW_SOLUTION = "s"
    HIDE_SOLUTION = "h"
    SAVE = "S"
    COLORS = "c"
    QUIT = "q"

    def message(self, ctx: Context) -> str:
        match self:
            case Event.GENERATE:
                return f"Generated maze (seed: {ctx.maze_generator.seed})"
            case Event.SHOW_SOLUTION:
                return f"Solved maze (seed: {ctx.maze_generator.seed})"
            case Event.HIDE_SOLUTION:
                return f"Hidden solution (seed: {ctx.maze_generator.seed})"
            case Event.SAVE:
                return (
                    f"Saved solution to '{ctx.config.output_file}' "
                    f"(seed: {ctx.maze_generator.seed})"
                )
            case Event.COLORS:
                return f"Changed colors (seed: {ctx.maze_generator.seed})"
            case Event.QUIT:
                return f"Quit (seed: {ctx.maze_generator.seed})"

    def to_string(self) -> str:
        match self:
            case Event.GENERATE:
                return "[g]enerate"
            case Event.SHOW_SOLUTION:
                return "[s]how"
            case Event.HIDE_SOLUTION:
                return "[h]ide"
            case Event.SAVE:
                return "[S]ave"
            case Event.COLORS:
                return "[c]olor"
            case Event.QUIT:
                return "[q]uit"


@dataclass
class StateMachine:
    transitions: dict[
        tuple[State, Event],
        tuple[State, Action[Context]],
    ] = field(
        default_factory=dict[
            tuple[State, Event],
            tuple[State, Action[Context]],
        ],
    )

    def add_transition(
        self,
        from_state: State,
        event: Event,
        to_state: State,
        func: Action[Context],
    ) -> None:
        self.transitions[from_state, event] = (to_state, func)

    def next_transition(
        self,
        state: State,
        event: Event,
    ) -> tuple[State, Action[Context]]:
        try:
            return self.transitions[state, event]
        except KeyError as error:
            raise InvalidTransition(
                f"Can not {event.name} when {state.name}",
            ) from error

    def handle(self, ctx: Context, state: State, event: Event) -> State:
        next_state, action = self.next_transition(state, event)

        action(ctx)

        ctx.maze_generator.display()

        print(event.message(ctx))

        if next_state is not State.QUIT:
            print()
            print(
                " | ".join([
                    e.to_string()
                    for s, e in self.transitions
                    if s == next_state
                ]),
            )

        return next_state

    def transition(
        self,
        from_state: State,
        event: Event,
        to_state: State,
    ) -> Callable[[Action[Context]], Action[Context]]:
        def decorator(func: Action[Context]) -> Action[Context]:
            self.add_transition(from_state, event, to_state, func)
            return func

        return decorator


STATE_MACHINE: StateMachine = StateMachine()


@STATE_MACHINE.transition(State.GENERATE, Event.GENERATE, State.GENERATE)
@STATE_MACHINE.transition(State.SOLVE, Event.GENERATE, State.GENERATE)
@STATE_MACHINE.transition(State.SAVE, Event.GENERATE, State.GENERATE)
def do_generate(ctx: Context) -> None:
    ctx.maze_generator = MazeGenerator.from_config(ctx.config)

    if ctx.config.animation:
        ctx.maze_generator.display()

    ctx.maze_generator.generate(ctx.config.perfect, ctx.config.seed)


@STATE_MACHINE.transition(State.GENERATE, Event.SHOW_SOLUTION, State.SOLVE)
def do_solve(ctx: Context) -> None:
    ctx.maze_generator.solve(ctx.config.algorithm)


@STATE_MACHINE.transition(State.SOLVE, Event.SAVE, State.SAVE)
def do_save(ctx: Context) -> None:
    ctx.maze_generator.save(ctx.config.output_file)


@STATE_MACHINE.transition(State.SOLVE, Event.SHOW_SOLUTION, State.SOLVE)
@STATE_MACHINE.transition(State.SAVE, Event.SHOW_SOLUTION, State.SAVE)
def do_show_solution(ctx: Context) -> None:
    if not ctx.maze_generator.renderer.show_solution():
        return


@STATE_MACHINE.transition(State.SOLVE, Event.HIDE_SOLUTION, State.SOLVE)
@STATE_MACHINE.transition(State.SAVE, Event.HIDE_SOLUTION, State.SAVE)
def do_hide_solution(ctx: Context) -> None:
    if not ctx.maze_generator.renderer.hide_solution():
        return


@STATE_MACHINE.transition(State.GENERATE, Event.COLORS, State.GENERATE)
@STATE_MACHINE.transition(State.SOLVE, Event.COLORS, State.SOLVE)
@STATE_MACHINE.transition(State.SAVE, Event.COLORS, State.SAVE)
def do_colors(ctx: Context) -> None:
    ctx.maze_generator.renderer.random_color(ctx.maze_generator.grid)


def do_colors_save(ctx: Context) -> None:
    ctx.maze_generator.renderer.random_color(ctx.maze_generator.grid)


@STATE_MACHINE.transition(State.GENERATE, Event.QUIT, State.QUIT)
@STATE_MACHINE.transition(State.SOLVE, Event.QUIT, State.QUIT)
@STATE_MACHINE.transition(State.SAVE, Event.QUIT, State.QUIT)
def do_quit(ctx: Context) -> None:
    pass
