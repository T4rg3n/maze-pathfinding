import random


def mazegen(length: int = 16, width: int = 16, seed: int = 42) -> list[list[str]]:
    """Generate a maze using the recursive backtracker (DFS) algorithm.

    Args:
        length: Number of rows in the maze grid.
        width: Number of columns in the maze grid.
        seed: Random seed for reproducibility.

    Returns:
        A 2D list of strings where '#' is a wall and '.' is an open path.
        'S' marks the start (top-left cell) and 'G' marks the goal (bottom-right cell).
    """
    if length < 3 or width < 3:
        raise ValueError("Maze dimensions must be at least 3x3.")

    rng = random.Random(seed)

    # Initialise every cell as a wall
    maze = [['#'] * width for _ in range(length)]

    # Interior cells visited during DFS sit at odd-indexed positions so that
    # carving a passage between two cells removes the wall between them.
    visited: set[tuple[int, int]] = set()

    def carve(row: int, col: int) -> None:
        visited.add((row, col))
        maze[row][col] = '.'

        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        rng.shuffle(directions)

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 1 <= nr < length - 1 and 1 <= nc < width - 1 and (nr, nc) not in visited:
                # Remove the wall between the current cell and the neighbour
                maze[row + dr // 2][col + dc // 2] = '.'
                carve(nr, nc)

    # Begin carving from the top-left interior cell
    carve(1, 1)

    # Place start and goal markers
    maze[1][1] = 'S'
    last_row = max(range(1, length - 1, 2))
    last_col = max(range(1, width - 1, 2))
    maze[last_row][last_col] = 'G'

    return maze
