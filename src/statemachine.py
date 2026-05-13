from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum, StrEnum, auto

from src.config import Config
from src.mazegen import MazeGenerator
from src.mazegen.render.ascii_renderer import AsciiRenderer

type Action[C] = Callable[[C], None]


class InvalidTransition(Exception):
    pass


@dataclass
class Context:
    maze_generator: MazeGenerator
    config: Config


class State(Enum):
    GENERATED = auto()
    SOLVED = auto()
    SOLVED_HIDDEN = auto()
    SOLVED_SHOWN = auto()
    SAVED_HIDDEN = auto()
    SAVED_SHOWN = auto()
    QUIT = auto()


class Event(StrEnum):
    GENERATE = "g"
    SOLVE = "o"
    HIDE_SOLUTION = "h"
    SHOW_SOLUTION = "s"
    SAVE = "a"
    COLORS = "c"
    QUIT = "q"

    def message(self, ctx: Context) -> str:
        match self:
            case Event.GENERATE:
                return f"Generated maze (seed: {ctx.maze_generator.seed})"
            case Event.SOLVE:
                return f"Solved maze (seed: {ctx.maze_generator.seed})"
            case Event.HIDE_SOLUTION:
                return f"Hidden solution (seed: {ctx.maze_generator.seed})"
            case Event.SHOW_SOLUTION:
                return f"Shown solution (seed: {ctx.maze_generator.seed})"
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
            case Event.SOLVE:
                return "s[o]lve"
            case Event.HIDE_SOLUTION:
                return "[h]ide"
            case Event.SHOW_SOLUTION:
                return "[s]how"
            case Event.SAVE:
                return "s[a]ve"
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
            events = []
            for s, e in self.transitions:
                if s != next_state:
                    continue

                if (
                    e is Event.HIDE_SOLUTION
                    and not ctx.maze_generator.renderer.is_solution_shown()
                ):
                    continue

                if (
                    e is Event.SHOW_SOLUTION
                    and ctx.maze_generator.renderer.is_solution_shown()
                ):
                    continue

                events.append(e)

            print()
            print(
                " | ".join([e.to_string() for e in events]),
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


@STATE_MACHINE.transition(State.GENERATED, Event.GENERATE, State.GENERATED)
@STATE_MACHINE.transition(State.SOLVED, Event.GENERATE, State.GENERATED)
@STATE_MACHINE.transition(State.SOLVED_HIDDEN, Event.GENERATE, State.GENERATED)
@STATE_MACHINE.transition(State.SOLVED_SHOWN, Event.GENERATE, State.GENERATED)
@STATE_MACHINE.transition(State.SAVED_HIDDEN, Event.GENERATE, State.GENERATED)
@STATE_MACHINE.transition(State.SAVED_SHOWN, Event.GENERATE, State.GENERATED)
def do_generate(ctx: Context) -> None:
    ctx.maze_generator = MazeGenerator(
        ctx.config.entry,
        ctx.config.exit,
        ctx.config.width,
        ctx.config.height,
    )
    ctx.maze_generator.renderer = AsciiRenderer.from_config(ctx.config)

    if ctx.config.animation:
        ctx.maze_generator.display()

    ctx.maze_generator.generate(ctx.config.perfect, ctx.config.seed)


@STATE_MACHINE.transition(State.GENERATED, Event.SOLVE, State.SOLVED)
def do_solve(ctx: Context) -> None:
    ctx.maze_generator.solve(ctx.config.algorithm)


@STATE_MACHINE.transition(State.SOLVED, Event.SAVE, State.SAVED_SHOWN)
@STATE_MACHINE.transition(State.SOLVED_HIDDEN, Event.SAVE, State.SAVED_HIDDEN)
@STATE_MACHINE.transition(State.SOLVED_SHOWN, Event.SAVE, State.SAVED_SHOWN)
def do_save(ctx: Context) -> None:
    ctx.maze_generator.save(ctx.config.output_file)


@STATE_MACHINE.transition(
    State.SOLVED_HIDDEN,
    Event.SHOW_SOLUTION,
    State.SOLVED_SHOWN,
)
@STATE_MACHINE.transition(
    State.SAVED_HIDDEN,
    Event.SHOW_SOLUTION,
    State.SAVED_SHOWN,
)
def do_show_solution(ctx: Context) -> None:
    ctx.maze_generator.renderer.show_solution()


@STATE_MACHINE.transition(
    State.SOLVED,
    Event.HIDE_SOLUTION,
    State.SOLVED_HIDDEN,
)
@STATE_MACHINE.transition(
    State.SOLVED_SHOWN,
    Event.HIDE_SOLUTION,
    State.SOLVED_HIDDEN,
)
@STATE_MACHINE.transition(
    State.SAVED_SHOWN,
    Event.HIDE_SOLUTION,
    State.SAVED_HIDDEN,
)
def do_hide_solution(ctx: Context) -> None:
    ctx.maze_generator.renderer.hide_solution()


@STATE_MACHINE.transition(State.GENERATED, Event.COLORS, State.GENERATED)
@STATE_MACHINE.transition(State.SOLVED, Event.COLORS, State.SOLVED)
@STATE_MACHINE.transition(
    State.SOLVED_HIDDEN,
    Event.COLORS,
    State.SOLVED_HIDDEN,
)
@STATE_MACHINE.transition(State.SOLVED_SHOWN, Event.COLORS, State.SOLVED_SHOWN)
@STATE_MACHINE.transition(State.SAVED_HIDDEN, Event.COLORS, State.SAVED_HIDDEN)
@STATE_MACHINE.transition(State.SAVED_SHOWN, Event.COLORS, State.SAVED_SHOWN)
def do_colors(ctx: Context) -> None:
    ctx.maze_generator.renderer.random_color(ctx.maze_generator.grid)


@STATE_MACHINE.transition(State.GENERATED, Event.QUIT, State.QUIT)
@STATE_MACHINE.transition(State.SOLVED, Event.QUIT, State.QUIT)
@STATE_MACHINE.transition(State.SOLVED_HIDDEN, Event.QUIT, State.QUIT)
@STATE_MACHINE.transition(State.SOLVED_SHOWN, Event.QUIT, State.QUIT)
@STATE_MACHINE.transition(State.SAVED_HIDDEN, Event.QUIT, State.QUIT)
@STATE_MACHINE.transition(State.SAVED_SHOWN, Event.QUIT, State.QUIT)
def do_quit(ctx: Context) -> None:
    pass
