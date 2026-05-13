_This project has been created as part of the 42 curriculum by ilclaass, tkunugi._

# Description

42 Next common core Python project.
Create own maze generator and display its result.

## Configuration

The configuration file contains one option per line, in the format: `OPTION=value`.
Empty lines and lines starting with a `#` are ignored.

Example:

```
WIDTH=18
HEIGHT=18
ENTRY=0,0
EXIT=17,17

OUTPUT_FILE=maze.txt
PERFECT=True
ALGORITHM=A*
#SEED=42

#ANIMATION=True
#ANIMATION_SPEED=100
#BACKGROUND_COLOR=white
#WALL_COLOR=black
#ENTRY_COLOR=red
#EXIT_COLOR=green
#FORTY_TWO_COLOR=magenta
#SOLUTION_COLOR=yellow
#ANIMATION_COLOR=blue
```

## Algorithms

### Generator

#### Depth-First Search (DFS)
<!-- TODO -->
Depth-First Search is well suited for maze generation because it naturally creates:
* long corridors
* branching paths
* organic maze structures

Random neighbor selection ensures that different seeds generate different maze layouts while still preserving valid maze connectivity.


#### Imperfect

After generating the perfect maze, the maze is divided into four quadrants using one horizontal and one vertical center line.
Additional walls are selectively removed between quadrants to create loops and multiple possible paths.
Before removing a wall, the algorithm checks that the change does not create an open area larger than 3×3 cells, helping preserve the overall maze structure.

### Solver

#### Depth-First Search (DFS)
<!-- TODO -->
Depth-First Search is a natural choice for solving mazes because it explores paths thoroughly before backtracking. This approach is particularly effective for:

Finding complete solutions – DFS will eventually reach the exit if a path exists.
Exploring branches – By following one path to its end, DFS reveals dead ends and alternative routes systematically.
Memory efficiency – DFS only needs to remember the current path, making it lightweight for large mazes.


#### Breadth-First Search (BFS)
<!-- TODO -->
Breadth-First Search is ideal for solving mazes when the goal is to find the shortest path from start to finish. BFS explores the maze level by level, ensuring that all positions at a given distance are visited before moving further. This makes it particularly suited for:

Guaranteed shortest paths – BFS always finds the path with the fewest steps.
Systematic exploration – It evenly examines all branches before going deeper, preventing missed paths.
Predictable behavior – BFS produces consistent solutions for the same maze, independent of randomness.

#### A\*
A\* was chosen as the solver because it is both optimal (always finds the shortest path) and efficient (explores fewer cells than a naive search by using a heuristic).

A\* assigns each cell a priority score:

$f(n) = g(n) + h(n)$

$g(n)$ — number of steps from the entry to cell $n$
$h(n)$ — estimated distance from $n$ to the exit (heuristic)

By always expanding the cell with the lowest $f(n)$ first, A\* focuses the search toward the exit instead of exploring in all directions equally.

Choosing the right heuristic

The heuristic $h(n)$ must match the movement rules of the map.

On a free map where diagonal movement is allowed, Euclidean distance is appropriate:  
$h(n) = √(dx² + dy²)$

In a maze, however, movement is restricted to four cardinal directions (north, east, south, west) — no diagonal steps are possible.
Manhattan distance fits this constraint exactly:  
$h(n) = |dx| + |dy|$

Using Manhattan distance here ensures the heuristic is admissible — it never overestimates the actual number of steps — which guarantees A\* always finds the shortest path.


# Instructions

### Usage

```python
maze_generator = MazeGenerator(src=(0, 0), dest=(19, 19), width=20, height=20)
maze_generator.generate(perfect=True, seed=None)
maze_generator.solve("A*")
print(maze_generator.solution)
```

---

### Build the package

Generate the distributable package files:

```bash
make build
```

This creates the following packages:

- `mazegen-1.0.0-py3-none-any.whl`
- `mazegen-1.0.0.tar.gz`

---

### Install the package

Install from the generated wheel:

```bash
pip install ./mazegen-1.0.0-py3-none-any.whl
```

Or install from the source archive:

```bash
pip install ./mazegen-1.0.0.tar.gz
```

---

### Run the program

```bash
make run
```

---

### Debug mode

```bash
make debug
```

---

### Run tests

```bash
make test
```

---

### Linting and formatting

Run lint checks:

```bash
make lint
```

Run strict linting and type checking:

```bash
make lint-strict
```

Format the code:

```bash
make format
```

---

### Clean generated files

```bash
make clean
```

# Resources

We used the following resources during development:

- [A\* search algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm)
- [Heuristics](https://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html)
- [The State Pattern in Python (video)](https://www.youtube.com/watch?v=OeirQdzYdnc)

## How AI was used

- Ensured the understanding of the algorithm was correct.
- Explored and gained a better understanding of Python built-in modules.
- Improved English writing.

# Project management

## Roles

We both worked on most of the code, but each of us worked more on certain parts of the codebase.

ilclaass:

- config
- grid
- DFS generator, solver
- BFS solver
- rendering

tkunugi:

- config
- state machine
- imperfect generator
- A\* solver

## Planning

<!-- TODO -->

## Reflection

<!-- TODO -->

## Tools

- `uv`: package and project manager
- `ruff` and `ty`: linting and formatting
- `pytest`: run tests
