# Copilot Instructions for maze-pathfinding

## Project Overview

This repository implements maze generation and pathfinding algorithms in Python. The project explores classic and modern algorithms for navigating through mazes, including but not limited to BFS, DFS, A*, and Dijkstra's algorithm.

## Tech Stack

- **Language**: Python 3
- **Testing**: pytest
- **Linting/Formatting**: Follow PEP 8 conventions; use `ruff` for linting if available

## Repository Structure

```
maze-pathfinding/
├── .github/                  # GitHub configuration and Copilot instructions
├── README.md                 # Project documentation
└── ...                       # Source files and tests
```

## Coding Conventions

- Follow [PEP 8](https://peps.python.org/pep-0008/) for all Python code.
- Use descriptive variable and function names (e.g., `start_node`, `find_shortest_path`).
- Prefer type hints for function signatures.
- Keep functions small and focused on a single responsibility.
- Document public functions and classes with docstrings.

## Maze Representation

- Mazes are typically represented as 2D grids (lists of lists or NumPy arrays).
- Cells are either walls (`1`) or open paths (`0`).
- Positions are represented as `(row, col)` tuples.

## Algorithms

When implementing pathfinding algorithms:
- Each algorithm should be in its own module or clearly separated function.
- Return the path as a list of `(row, col)` tuples from start to end, or `None` if no path exists.
- Include the start and end positions in the returned path.

## Testing

- Place tests in a `tests/` directory, mirroring the structure of the source code.
- Use `pytest` to run tests: `pytest tests/`
- Test edge cases: no path exists, start equals end, single-cell maze.
- Test correctness of returned paths (verify path continuity and that start/end are included).

## Development Setup

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt  # if available

# Run tests
pytest tests/
```

## Pull Request Guidelines

- Include a clear description of the algorithm or feature being added or changed.
- Ensure all tests pass before submitting.
- Add tests for any new algorithms or utility functions.
