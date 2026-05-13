"""The main A-Maze-ing program."""

import select
import sys
import termios
from collections.abc import Callable
from dataclasses import dataclass, field, fields
from enum import Enum, StrEnum, auto
from types import TracebackType
from typing import Any, Literal, Self, get_args, get_type_hints

from mazegen import MazeGenerator
from mazegen.color import Color
from mazegen.render.ascii_renderer import AsciiRenderer
from mazegen.render.config import RenderConfig

type ParserFn = Callable[[str], Any]

PARSERS: dict[str, ParserFn] = {}


class ConfigError(Exception):
    pass


def register_parser(fn: ParserFn) -> ParserFn:
    return_type = get_type_hints(fn).get("return")

    if return_type is None:
        raise ConfigError(f"parser function `{fn}` returns `None`")

    if PARSERS.get(return_type) is not None:
        raise ConfigError(
            f"parser function already defined for `{return_type}`",
        )

    PARSERS[return_type] = fn

    return fn


@register_parser
def parse_int(value: str) -> int:
    try:
        return int(value)
    except ValueError as error:
        raise ConfigError(f"invalid integer: `{value}`") from error


@register_parser
def parse_int_tuple(value: str) -> tuple[int, int]:
    split_value = value.split(",", 1)

    if len(split_value) != 2:
        raise ConfigError("expected two values seperated by a comma")

    try:
        x = parse_int(split_value[0])
    except ConfigError as error:
        raise error

    try:
        y = parse_int(split_value[1])
    except ConfigError as error:
        raise error

    return (x, y)


@register_parser
def parse_bool(value: str) -> bool:
    if value == "True":
        return True

    if value == "False":
        return False

    raise ConfigError(f"invalid boolean literal: `{value}`")


@register_parser
def parse_str(value: str) -> str:
    return value


@register_parser
def parse_algorithm(value: str) -> Literal["DFS", "BFS", "A*"]:
    match value:
        case "DFS":
            return "DFS"
        case "BFS":
            return "BFS"
        case "A*":
            return "A*"
        case _:
            raise ConfigError(f"invalid algorithm: `{value}`")


@register_parser
def parse_color(value: str) -> Color:
    try:
        return Color(value)
    except (KeyError, ValueError) as error:
        raise ConfigError(f"invalid color: `{value}`") from error


def get_parser(key: str) -> ParserFn:
    field_names: list[str] = [field.name.upper() for field in fields(Config)]
    field_types: list[Any] = [field.type for field in fields(Config)]

    try:
        index = field_names.index(key)
    except ValueError as error:
        raise ConfigError(f"invalid key: `{key}`") from error

    field_type = field_types[index]
    type_args = get_args(field_type)

    if len(type_args) <= 1 or type_args[-1] is not type(None):
        return PARSERS[field_type]

    parts = tuple(arg for arg in type_args)

    if len(parts) == 1:
        return PARSERS[parts[0]]

    union = parts[0]

    for part in parts[1:-1]:
        union |= part

    return PARSERS[union]


def parse_line(config: dict[str, Any], line: str) -> None:
    stripped_line = line.strip()

    if not stripped_line or stripped_line.startswith("#"):
        return

    split_line = stripped_line.split("=", 1)

    if len(split_line) != 2:
        raise ConfigError("expected two values seperated by =")

    key = split_line[0]
    value = split_line[1]

    try:
        parser = get_parser(key)
    except ConfigError as error:
        raise error

    try:
        result = parser(value)
    except ConfigError as error:
        raise error

    config[key.lower()] = result


@dataclass
class Config:
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str

    perfect: bool
    algorithm: Literal["DFS", "BFS", "A*"] | None = None
    seed: int | None = None

    animation: bool = False
    animation_speed: int = 100
    background_color: Color = Color.BLACK
    wall_color: Color = Color.WHITE
    entry_color: Color = Color.GREEN
    exit_color: Color = Color.RED
    forty_two_color: Color = Color.YELLOW
    solution_color: Color = Color.MAGENTA
    animation_color: Color = Color.BLUE

    @classmethod
    def from_file(cls, filepath: str) -> Self:
        try:
            with open(filepath, encoding="utf-8") as file:
                config: dict[str, Any] = {}

                for line in file:
                    parse_line(config, line)

                try:
                    cfg = cls(**config)
                except KeyError as error:
                    raise ConfigError("missing key/value pair") from error

                try:
                    cfg.validate()
                except ConfigError as error:
                    raise error

                return cfg
        except OSError as error:
            raise ConfigError(f"failed to open file: `{filepath}`") from error

    def validate(self) -> None:
        if self.width <= 0:
            raise ConfigError(f"width must be positive: `{self.width}`")

        if self.height <= 0:
            raise ConfigError(f"height must be positive: `{self.height}`")

        if (
            self.entry[0] < 0
            or self.entry[0] >= self.width
            or self.entry[1] < 0
            or self.entry[1] >= self.height
        ):
            raise ConfigError(f"entry must be in grid range: `{self.entry}`")

        if (
            self.exit[0] < 0
            or self.exit[0] >= self.width
            or self.exit[1] < 0
            or self.exit[1] >= self.height
        ):
            raise ConfigError(f"exit must be in grid range: `{self.exit}`")

        if self.entry == self.exit:
            raise ConfigError(
                f"entry and exit must be different: `{self.entry}`",
            )

    def into_render_config(self) -> RenderConfig:
        return RenderConfig(
            self.animation,
            self.animation_speed,
            self.background_color,
            self.wall_color,
            self.entry_color,
            self.exit_color,
            self.forty_two_color,
            self.solution_color,
            self.animation_color,
        )


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
    ctx.maze_generator.renderer = AsciiRenderer(
        ctx.config.into_render_config(),
    )

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


class NonBlockingInput:
    def __enter__(self) -> None:
        self._old = termios.tcgetattr(sys.stdin)
        new = self._old
        new[3] &= ~termios.ECHO
        new[3] &= ~termios.ICANON
        termios.tcsetattr(sys.stdin, termios.TCSANOW, new)

    def __exit__(
        self,
        _type: type[BaseException] | None,
        _value: BaseException | None,
        _traceback: TracebackType | None,
    ) -> bool | None:
        termios.tcsetattr(sys.stdin, termios.TCSANOW, self._old)
        return None


def main() -> None:
    try:
        config = Config.from_file(sys.argv[1])
    except ConfigError as error:
        print(f"Config error: {error}")
        sys.exit(1)

    with NonBlockingInput():
        maze_generator = MazeGenerator(
            config.entry,
            config.exit,
            config.width,
            config.height,
        )
        maze_generator.renderer = AsciiRenderer(config.into_render_config())
        ctx = Context(maze_generator, config)
        current_state = State.GENERATED
        STATE_MACHINE.handle(ctx, current_state, Event.GENERATE)

        while current_state is not State.QUIT:
            read_fd, _, _ = select.select([sys.stdin], [], [], 0)
            if not read_fd:
                continue
            character = sys.stdin.read(1)
            if not character:
                break

            try:
                event = Event(character)
            except ValueError:
                continue

            try:
                current_state = STATE_MACHINE.handle(ctx, current_state, event)
            except InvalidTransition:
                continue


if __name__ == "__main__":
    # hide cursor
    print("\033[?25l")
    main()
