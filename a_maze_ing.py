"""The main A-Maze-ing program."""

import select
import sys
import termios
from types import TracebackType

from src.config import Config, ConfigError
from src.mazegen import MazeGenerator
from src.mazegen.render.ascii_renderer import AsciiRenderer
from src.statemachine import (
    STATE_MACHINE,
    Context,
    Event,
    InvalidTransition,
    State,
)


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
        maze_generator.renderer = AsciiRenderer.from_config(config)
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
