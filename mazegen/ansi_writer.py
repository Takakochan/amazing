import sys
from dataclasses import dataclass

from mazegen.cell import Cell
from mazegen.color import Color


@dataclass
class AnsiWriter:
    _buffer: str = ""
    _line: int = 1
    _column: int = 1

    def move_to_position(
        self,
        cell: Cell,
        line_offset: int = 0,
        column_offset: int = 0,
    ) -> None:
        self._line = cell.y * 3 + 2 + line_offset
        self._column = cell.x * 6 + 3 + column_offset

    def write(self, string: str) -> None:
        self._buffer += string

    def prepend_write(self, string: str) -> None:
        self._buffer = string + self._buffer

    def write_clear_screen(self) -> None:
        self.write("\033[2J\033[H")

    def write_clear_line(self) -> None:
        self.write("\033[2K")

    def write_hide_cursor(self) -> None:
        self.write("\033[?25l")

    def write_show_cursor(self) -> None:
        self.write("\033[?25h")

    def write_cursor_up(self, lines: int) -> None:
        self.write(f"\033[{lines}A")

    def write_cursor_down(self, lines: int) -> None:
        self.write(f"\033[{lines}B")

    def write_cursor_forward(self, columns: int) -> None:
        self.write(f"\033[{columns}C")

    def write_cursor_backward(self, columns: int) -> None:
        self.write(f"\033[{columns}D")

    def write_cursor_position(self, line: int, column: int) -> None:
        self.write(f"\033[{line};{column}H")

    def write_current_position(self) -> None:
        self.write_cursor_position(self._line, self._column)

    def write_color_pixel(self, color: Color, width: int = 1) -> None:
        PIXEL = "██"
        self.write(color.escape_code())
        self.write(PIXEL * width)

    def write_color_reset(self) -> None:
        self.write(Color.reset())

    def write_box(self, color: Color, width: int, height: int) -> None:
        self.write_current_position()

        for i in range(height):
            if i > 0:
                self.write_cursor_down(1)
                self.write_cursor_backward(2 * width)

            self.write_color_pixel(color, width)

    def flush(self) -> None:
        sys.stdout.write(self._buffer)
        sys.stdout.flush()
        self._buffer = ""
