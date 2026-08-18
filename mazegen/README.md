# mazegen

`mazegen` is a standalone, reusable maze-generation module built for the
A-Maze-ing project. It exposes a single class, `MazeGenerator`, that
generates rectangular mazes using an iterative depth-first search, with
support for both "perfect" mazes (a single path, no loops) and "playable"
Pac-Man-style boards (loops, guaranteed reachable corners and centre, and a
protected "42" pattern isolated at the centre of the grid).

It has no third-party dependencies: it only relies on the Python standard
library.

## Installation

Install the built wheel (or sdist) with pip, ideally inside a virtual
environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install mazegen-1.0.0-py3-none-any.whl
```

## 1. Instantiate and use: basic example

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
    width=15,
    height=15,
    entry=(0, 0),
    exit_cell=(14, 14),
)

maze.generate()          # perfect maze by default (perfect=True)

print(maze.to_hex())     # hexadecimal representation, one row per line
```

`generate()` must be called once after instantiation: it builds the wall
grid, carves the maze with DFS, and (if requested) turns it into a playable
board. `width` and `height` are in cells, and `entry` / `exit_cell` are
`(x, y)` coordinate tuples inside the grid.

## 2. Passing custom parameters (size, seed, playable mode)

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
    width=21,             # any positive width, in cells
    height=21,             # any positive height, in cells
    entry=(0, 0),
    exit_cell=(20, 20),
    seed=42,               # optional: reproducible generation
)

maze.generate(perfect=False)   # False -> playable Pac-Man-style board
                                # True (default) -> perfect maze, no loops
```

- `seed`: if omitted, a random seed is generated and stored on
  `maze.seed`, so you can always retrieve which seed produced a given
  maze (useful for reproducing or sharing a specific layout).
- `maze.regenerate()`: draws a brand new random seed and resets the
  internal random generator, without changing width/height/entry/exit.
  Call `generate()` again afterwards to actually build the new maze.
- `perfect=True` (default): the maze has exactly one path between any two
  reachable cells (no loops).
- `perfect=False`: extra passages are opened to create loops, and the four
  corners plus the centre cell are guaranteed to be reachable, so the
  board can be reused as a Pac-Man-like level.

## 3. Accessing the generated structure and a solution

### Raw structure

```python
maze.grid
```

`maze.grid` is the internal structure: a list of `height` rows, each a
list of `width` cells. Each cell is a `dict` with 4 boolean keys —
`"North"`, `"East"`, `"South"`, `"West"` — where `True` means that wall
side is closed. This is **not** the same format as the project's output
file; it is the live, mutable representation used internally.

Two read-only conversions are also available:

```python
maze.to_hex()          # str: one hexadecimal digit per cell, one row per
                        # line (bit 0=North, 1=East, 2=South, 3=West)

maze.grid_to_ints()     # list[list[int]]: same wall encoding as to_hex(),
                         # but as a 2D list of integers instead of a string
```

### Accessing a solution

```python
path_letters = maze.bfs()
# e.g. ['E', 'E', 'S', 'S', 'E', ...]

path_coords = maze.path_to_coords(path_letters)
# e.g. [(0, 0), (1, 0), (2, 0), (2, 1), ...]
```

`maze.bfs()` runs a breadth-first search from `maze.entry` to
`maze.exit_cell` and returns the shortest path as a list of direction
letters (`'N'`, `'E'`, `'S'`, `'W'`). `maze.path_to_coords()` turns that
list of letters into the actual list of `(x, y)` cell coordinates visited,
starting at `maze.entry`.

## Errors

`mazegen.MazeError` is raised when:

- The entry cell, the exit cell, or the DFS starting cell falls inside the
  protected "42" pattern.
- `maze.bfs()` is called with an entry or exit cell inside the "42"
  pattern.

```python
from mazegen import MazeGenerator, MazeError

try:
    maze = MazeGenerator(width=15, height=15, entry=(7, 6), exit_cell=(14, 14))
    maze.generate()
except MazeError as exc:
    print(f"Invalid maze configuration: {exc}")
```

## License

This module is released under the MIT License (see `LICENSE.md` at the
root of the repository), which explicitly allows reuse, modification, and
redistribution of this code by later, unrelated projects.