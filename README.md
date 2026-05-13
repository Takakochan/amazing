_This project has been created as part of the 42 curriculum by ilclaass, tkunugi._<br>

# Discription

42 Next commoncore Python project.  A-Maze-ing. 
Create own maze generator and display its result.

## MazeGenerator

### The algorythm what we have choosen for Maze generator

**Depth-First Search** algorithm for the perfect maze.

### What we have implement for imperfect maze generator

After generating the perfect maze, the maze is divided into four quadrants using one horizontal and one vertical center line.
Additional walls are selectively removed between quadrants to create loops and multiple possible paths.
Before removing a wall, the algorithm checks that the change does not create an open area larger than 3×3 cells, helping preserve the overall maze structure.

### Example

```python
maze_generator = MazeGenerator(src=(0, 0), dest=(19, 19), width=20, height=20)
maze_generator.generate(perfect=True, seed=None)
maze_generator.solve("A*")
print(maze_generator.solution)
```

## Solver
### A\* Algorithm

### Why A\*?

A\* was chosen as the solver because it is both optimal (always finds the shortest path) and efficient (explores fewer cells than a naive search by using a heuristic).

### How it works

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

<br>

## State Machine

### Overview

User interactions are managed by a state machine.
It separates what state the program is in from what to do when an event occurs, making the logic easy to extend.

At its core, the state machine is a lookup table mapping (state, event) pairs to (next state, action).

<!-- This pattern is widely used beyond games and CLIs — payment processing systems, for example, use the same approach to manage order lifecycles (e.g. pending → authorized → captured → refunded). -->

### Design

Transitions are registered with a decorator, keeping the definition and the action together:

```python
@STATE_MACHINE.transition(State.GENERATE, Event.SHOW_SOLUTION, State.SOLVE)
def do_solve(ctx: Context) -> None:
    ctx.maze_generator.solve(ctx.config.algorithm)
```

<br>

# Instructions

### Build the package

Generate the distributable package files:

```bash
make build
```

This creates both:

- `.whl`
- `.tar.gz`

package files at the root of the repository.

Example:

```bash
mazegen-1.0.0-py3-none-any.whl
```

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

### Resouce

[About A\* wikipedia](https://ja.wikipedia.org/wiki/A*)<br>
[Heuristics](https://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html)<br>
[The State Pattern in Python (video)](https://www.youtube.com/watch?v=OeirQdzYdnc)<br>

### How AI was used 
Ensured the understanding of the algorithm was correct.<br>
Explored and gained a better understanding of Python built-in modules.<br>
Improved English writing.<br>