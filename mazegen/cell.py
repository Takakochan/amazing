from dataclasses import dataclass

from mazegen.cell_value import CellValue


@dataclass
class Cell:
    x: int
    y: int
    value: CellValue
