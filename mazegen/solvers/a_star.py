from mazegen.cell import Cell
from mazegen.grid import Grid
from mazegen.cell_value import CellValue
from mazegen.solvers.base import Solver
import heapq


class PriorityQue():
    def __init__(self):
        self._heap: List[Tuple[int, Cell]] = []
        self.counter: int = 0

    def push(self, priority: int, cell: Cell) -> None:
        heapq.heappush(self._heap, (priority, cell))

    
    def pop(self) -> Cell:
        if not self._heap:
            raise Exception("Open set is empty → path not found")  # Debug
        priority, cell = heapq.heappop(self._heap)
        print("POP:", cell)
        return cell

    def is_empty(self)-> bool:
        if len(self._heap) == 0:
            return True
        return False

class SolverAstar(Solver):
    def solve(
        self,
        grid: Grid,
        entry: Cell,
        exit: Cell,
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
            print("CURRENT", current)
            if (current.x, current.y) in closed_set: # 入っていたらもう見てる
                continue
            closed_set.add((current.x, current.y))
        #TODO 隣セルの処理
            n = 1
            for neighbor in grid.get_reachable_unmarked_neighbors(current):
                print(f"In the for loop {n}th time")
                n += 1
                temp = g_score[current.x, current.y] + 1
                g_score[neighbor.x, neighbor.y] = temp
                grid.set_parent(neighbor, current)
                open_set.push(f_score(temp, manhattan_heuristic(neighbor, exit)), neighbor)
                print("PUSH:", neighbor)

            current = exit
        while current is not entry:
            if current != exit:
                grid.set_cell_value(current, CellValue.SOLUTION)

            parent = grid.get_parent(current)
            if parent is None:
                break

            current = parent

            grid.display()

        grid.reset_cell_markings()
        grid.unset_parents()



def f_score(g_score: int, manhattan_heuristic: int) -> int:
    return g_score + manhattan_heuristic
        

def manhattan_heuristic(current: Cell, exit: Cell) -> int:
    return abs(current.x - exit.x) + abs(current.y - exit.y)




