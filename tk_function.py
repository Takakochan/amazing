from abc import abstractmethod, ABC
from typing import Any


class ConfigValue(ABC):
    @abstractmethod
    @staticmethod
    def parse(line: Any) -> Any:
        pass


class IntValue(ConfigValue):
    @staticmethod
    def parse(line: str) -> int:
        return int(line.strip())


class StrValue(ConfigValue):
    @staticmethod
    def parse(line: str) -> str:
        return line.strip()


class BoolValue(ConfigValue):
    @staticmethod
    def parse(line: str) -> bool:
        striped_line = line.strip()
        if striped_line == "True":
            return True
        elif striped_line == "False":
            return False
        else:
            raise ValueError("Invalid input, must be True or False")


class PositonValue(ConfigValue):
    @staticmethod
    def parse(line: str) -> tuple[int, int]:
        split_line = line.split(",")
        # TODO: check invalid input
        x = IntValue.parse(split_line[0])
        y = IntValue.parse(split_line[1])

        return (x, y)


def read_config():
    with open("config.txt", "r") as file:
        for line in file:
            if line.strip().startswith("#"):
                continue

            split_line = line.split("=")
            # TODO: check invalid input
            key = split_line[0]
            value = split_line[1]
