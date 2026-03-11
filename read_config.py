from abc import ABC, abstractmethod


class ConfigValue(ABC):
    @staticmethod
    @abstractmethod
    def parse(value: str) -> int | str | bool | tuple[int, int]:
        pass


class IntValue(ConfigValue):
    @staticmethod
    def parse(value: str) -> int:
        return int(value)


class PositonValue(ConfigValue):
    @staticmethod
    def parse(value: str) -> tuple[int, int]:
        split_value = value.split(",", 1)
        # TODO: check invalid input
        if len(split_value) != 2:
            raise ValueError("Potisional value must contain 2 integer")
        x = IntValue.parse(split_value[0])
        y = IntValue.parse(split_value[1])

        return (x, y)


class BoolValue(ConfigValue):
    @staticmethod
    def parse(value: str) -> bool:
        if value == "True":
            return True

        if value == "False":
            return False

        raise ValueError("Invalid input, must be True or False")


class StrValue(ConfigValue):
    @staticmethod
    def parse(value: str) -> str:
        return value


def parse_line(
    config: dict,
    maze_dict: dict,
    line: str,
) -> None:
    stripped_line = line.strip()

    if not stripped_line or stripped_line.startswith("#"):
        return

    split_line = stripped_line.split("=", 1)
    # TODO: check invalid input
    key = split_line[0]
    value = split_line[1]

    parser = config.get(key)

    if parser is None:
        raise ValueError(f"Invalid key: {key}")

    # TODO: catch error
    result = parser.parse(value)

    maze_dict[key.lower()] = result


def read_config(filename: str) -> dict:
    config: dict = {}

    config["HEIGHT"] = IntValue
    config["WIDTH"] = IntValue
    config["ENTRY"] = PositonValue
    config["EXIT"] = PositonValue
    config["OUTPUT_FILE"] = StrValue
    config["PERFECT"] = BoolValue

    with open(filename, encoding="utf-8") as file:
        maze_dict: dict = {}
        for line in file:
            # TODO: catch error
            parse_line(config, maze_dict, line)
        return maze_dict


if __name__ == "__main__":
    try:
        maze_dict = read_config("badconfig.txt")
        # TODO: check for missing key/value pairs
        # TODO: convert to Maze class
        print(f"{maze_dict}")
    except OSError as error:
        print(f"{error}")
