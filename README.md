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

#### Imperfect

After generating the perfect maze, the maze is divided into four quadrants using one horizontal and one vertical center line.
Additional walls are selectively removed between quadrants to create loops and multiple possible paths.
Before removing a wall, the algorithm checks that the change does not create an open area larger than 3×3 cells, helping preserve the overall maze structure.

### Solver

#### Depth-First Search (DFS)

<!-- TODO -->

#### Breadth-First Search (BFS)

<!-- TODO -->

#### A\*

<!-- TODO -->

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
