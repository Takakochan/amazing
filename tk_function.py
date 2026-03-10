from abc import ABC, abstractmethod


class ConfigValue(ABC):
    @abstractmethod
    @staticmethod
    def parse(value: str) -> int | str | bool | tuple[int, int]:
        pass


class IntValue(ConfigValue):
    @staticmethod
    def parse(value: str) -> int:
        return int(value)


class StrValue(ConfigValue):
    @staticmethod
    def parse(value: str) -> str:
        return value


class BoolValue(ConfigValue):
    @staticmethod
    def parse(value: str) -> bool:
        if value == "True":
            return True

        if value == "False":
            return False

        raise ValueError("Invalid input, must be True or False")


class PositonValue(ConfigValue):
    @staticmethod
    def parse(value: str) -> tuple[int, int]:
        split_value = value.split(",")
        # TODO: check invalid input
        x = IntValue.parse(split_value[0])
        y = IntValue.parse(split_value[1])

        return (x, y)


def read_config():
    with open("config.txt") as file:
        for line in file:
            stripped_line = line.strip()

            if stripped_line.startswith("#"):
                continue

            split_line = stripped_line.split("=")
            # TODO: check invalid input
            key = split_line[0]
            value = split_line[1]
