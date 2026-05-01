"""The main A-Maze-ing program."""

import select
import sys
import termios
from types import TracebackType

from config import Config, ConfigError
from mazegen import MazeGenerator
from statemachine import (
    Event,
    InvalidTransition,
    MazeContext,
    MazeState,
    sm,
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
        print(f"Error {error}")
        sys.exit(1)

    with NonBlockingInput():
        # state: State = GenerateState.from_config(config)
        ctx = MazeContext(MazeGenerator.from_config(config), config)
        if config.animation:
            ctx.maze_generator.display()
        ctx.maze_generator.generate(config.perfect, config.seed)
        ctx.maze_generator.display()
        print(f"Generated maze (seed: {ctx.maze_generator.seed})")
        print()
        print("[g]enerate | [s]olve | [q]uit | [c]olor")
        current_state = MazeState.GENERATE
        while True:
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

            if event is Event.QUIT:
                break

            # state = state.on_event(event)
            try:
                current_state = sm.handle(ctx, current_state, event)
            except InvalidTransition:
                continue


if __name__ == "__main__":
    # hide cursor
    print("\033[?25l")
    main()
