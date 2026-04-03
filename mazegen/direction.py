from enum import StrEnum, auto


class Direction(StrEnum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()

    def into_file_format(self) -> str:
        match self:
            case Direction.NORTH:
                return "N"
            case Direction.EAST:
                return "E"
            case Direction.SOUTH:
                return "S"
            case Direction.WEST:
                return "W"
