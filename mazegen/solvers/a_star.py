from mazegen.cell import Cell
from mazegen.grid import Grid
from mazegen.solvers.base import Solver
import heapq


class SolverAStar(Solver):
    def solve(
        grid: Grid,
        entry: Cell,
        exit: Cell,  # noqa: A002
    ) -> None:
        pass

class PriorityQue():
    def __init__(self):
        self._heap = []
    
    def push(self, priority: int, cell: Cell):

    
    # def pop(self) -> Cell:
    #     return

    # def is_empty(self)-> bool:
    #     return 



def f_scor(g_score: int, manhattan_heuristic: int) -> int:
    return g_score + manhattan_heuristic
        
def manhattan_heuristic(current: Cell, exit: Cell) -> int:
    return abs(current.x - exit.x) + abs(current.y - exit.y)

dict[tuple[int, int], int]