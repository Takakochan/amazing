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


def read_config(filename: str) -> None:
    config = {}

    config["HEIGHT"] = IntValue
    config["WIDTH"] = IntValue
    config["ENTRY"] = PositonValue
    config["EXIT"] = PositonValue
    config["OUTPUT_FILE"] = StrValue
    config["PERFECT"] = BoolValue

    try:
        with open(filename, encoding="utf-8") as file:
            for line in file:
                stripped_line = line.strip()

                if not stripped_line or stripped_line.startswith("#"):
                    continue

                split_line = stripped_line.split("=", 1)
                # TODO: check invalid input
                key = split_line[0]
                value = split_line[1]

                parser = config.get(key)

                if parser is None:
                    raise ValueError(f"Invalid key: {key}")

                result = parser.parse(value)

                print(f"{key}={value} -> {result}")
    except OSError as error:
        print(f"{error}")


if __name__ == "__main__":
    read_config("config.txt")
