"""The main A-Maze-ing program."""

import select
import sys
import termios
from types import TracebackType

from config import Config, ConfigError
from state import Event, GenerateState


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


def main() -> None:
    try:
        config = Config.from_file(sys.argv[1])
    except ConfigError as error:
        raise error

    with NonBlockingInput():
        state = GenerateState.from_config(config)

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

            state = state.on_event(event)


if __name__ == "__main__":
    # hide cursor
    print("\033[?25l")
    main()
