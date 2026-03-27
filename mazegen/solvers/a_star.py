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
        open_set = PriorityQue()
        """ hopeful condidates list which we gonna check """
        open_set.push(0, entry)
        g_score = {(entry.x, entry.y): 0}
        """g_score: actual cost sntry to current cell"""

        closed_set = set()
        while not open_set.is_empty():
            """Main loop"""
            current = open_set.pop() # 一番有望なのをPOP
            if (current.x, current.y) in closed_set: # 入っていたらもう見てる
                continue
            closed_set.add((current.x, current.y))
        #TODO 隣セルの処理
        Grid.get_reachable_unmarked_neighbors(current)???

class PriorityQue():
    def __init__(self):
        self._heap: List[Tuple[int, Cell]] = []
    
    def push(self, priority: int, cell: Cell) -> None:
    
    def pop(self) -> Cell:
        return

    def is_empty(self)-> bool:
        if self._heap == 0:
            return True
        return False



def f_score(g_score: int, manhattan_heuristic: int) -> int:
    return g_score + manhattan_heuristic
        
def manhattan_heuristic(current: Cell, exit: Cell) -> int:
    return abs(current.x - exit.x) + abs(current.y - exit.y)

dict[tuple[int, int], int]


