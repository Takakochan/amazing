# THIS FILE HAS BEEN REPLACED BY `CONFIG.PY`


# from abc import ABC, abstractmethod
#
#
# class ConfigValue(ABC):
#     @staticmethod
#     @abstractmethod
#     def parse(value: str) -> int | str | bool | tuple[int, int]:
#         pass
#
#
# class IntValue(ConfigValue):
#     @staticmethod
#     def parse(value: str) -> int:
#         try:
#             return int(value)
#         except ValueError:
#             raise ValueError(f"invalid integer: '{value}'")
#
#
# class PositionValue(ConfigValue):
#     @staticmethod
#     def parse(value: str) -> tuple[int, int]:
#         split_value = value.split(",", 1)
#         # TODO: check invalid input
#         if len(split_value) != 2:
#             raise ValueError("Potisional value must contain 2 integers")
#         x = IntValue.parse(split_value[0])
#         y = IntValue.parse(split_value[1])
#
#         return (x, y)
#
#
# class BoolValue(ConfigValue):
#     @staticmethod
#     def parse(value: str) -> bool:
#         if value == "True":
#             return True
#
#         if value == "False":
#             return False
#
#         raise ValueError("Invalid input, must be True or False")
#
#
# class StrValue(ConfigValue):
#     @staticmethod
#     def parse(value: str) -> str:
#         return value
#
#
# def parse_line(
#     config: dict,
#     maze_dict: dict,
#     line: str,
# ) -> None:
#     stripped_line = line.strip()
#
#     if not stripped_line or stripped_line.startswith("#"):
#         return
#     split_line = stripped_line.split("=", 1)
#     # TODO: check invalid input
#     key = split_line[0]
#     value = split_line[1]
#     parser = config.get(key)
#     if parser is None:
#         raise ValueError(f"Invalid key: Missing Non-mandatory key: '{key}'")
#     result = parser.parse(value)
#     maze_dict[key.lower()] = result
#
#
# REQUIRED_KEYS = {'WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT'}
#
#
# def read_config(filename: str) -> dict:
#     config: dict = {}
#     config["HEIGHT"] = IntValue
#     config["WIDTH"] = IntValue
#     config["ENTRY"] = PositionValue
#     config["EXIT"] = PositionValue
#     config["OUTPUT_FILE"] = StrValue
#     config["PERFECT"] = BoolValue
#
#     try:
#         with open(filename, encoding="utf-8") as file:
#             maze_dict: dict = {}
#             for line in file:
#                 try:
#                     parse_line(config, maze_dict, line)
#                 except ValueError as e:
#                     print(f"Error: {e}")
#     except FileNotFoundError as e:
#         print(f"Error: {e}")
#     maze_keys = set(maze_dict.keys())
#     upper_maze_keys = {key.upper() for key in maze_keys}
#     missing_key = REQUIRED_KEYS - upper_maze_keys
#     if missing_key:
#         raise ValueError("Incomplete config values")
#     return maze_dict
#
#
# if __name__ == "__main__":
#     try:
#         maze_dict = read_config("config.txt")
#         # TODO: convert to Maze class
#         print(f"{maze_dict}")
#     except OSError as error:
#         print(f"{error}")
