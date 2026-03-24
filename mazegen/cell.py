from dataclasses import dataclass

from mazegen.cell_coordinate import CellCoordinate
from mazegen.cell_value import CellValue


@dataclass
class Cell(CellCoordinate):
    value: CellValue
