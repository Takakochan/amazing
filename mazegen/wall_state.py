"""The wall state."""

from enum import Enum


class WallState(Enum):
    """
    The state of a wall.

    Attributes:
        open: the wall is open
        closed: the wall is closed

    """

    OPEN = 0
    CLOSED = 1
