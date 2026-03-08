def dfs(maze: list[list[str]]) -> list[list[str]] | tuple[list[list[str]], list[tuple[int, int]]]:
    """
    Depth First Search algorithm to solve the maze.

    Uses a stack
    """
    stack = []
    visited: set[tuple[int, int]] = set()
    visit_order: list[tuple[int, int]] = [] # Used for animation

    # Find the start position (S)
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == "S":
                stack.append((row, col))
                break

    rows = len(maze)
    cols = len(maze[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up

    # Go down as much as we can, mark each cell visited
    while stack:
        row, col = stack.pop()
        if (row, col) in visited:
            continue
        visited.add((row, col))
        visit_order.append((row, col))

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                cell = maze[nr][nc]
                if (nr, nc) not in visited and cell in (".", "G"):
                    stack.append((nr, nc))

    return maze, visit_order