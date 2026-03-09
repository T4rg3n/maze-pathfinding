from collections import deque
import time


def bfs(maze: list[list[str]]) -> tuple[list[list[str]], list[tuple[int, int]], list[tuple[int, int]], float]:
    """
    Breadth First Search algorithm to solve the maze.

    Uses a queue (FIFO). Returns (maze, visit_order, solution_path, time_us).
    """
    start = time.perf_counter()
    queue: deque[tuple[int, int]] = deque()
    visited: set[tuple[int, int]] = set()
    visit_order: list[tuple[int, int]] = []
    parent: dict[tuple[int, int], tuple[int, int]] = {}

    # Find the start position (S)
    start_found = False
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == "S":
                queue.append((row, col))
                start_found = True
                break
        if start_found:
            break

    rows = len(maze)
    cols = len(maze[0])

    right = (0, 1)
    down = (1, 0)
    left = (0, -1)
    up = (-1, 0)
    directions = [right, down, left, up]

    while queue:
        row, col = queue.popleft()
        if (row, col) in visited:
            continue
        visited.add((row, col))
        visit_order.append((row, col))

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                cell = maze[nr][nc]
                if cell == ".":
                    if (nr, nc) not in parent:
                        parent[(nr, nc)] = (row, col)
                    queue.append((nr, nc))
                if cell == "G":
                    parent[(nr, nc)] = (row, col)
                    visit_order.append((nr, nc))
                    path_back: list[tuple[int, int]] = []
                    current = (nr, nc)
                    max_path_len = rows * cols
                    while current in parent and len(path_back) < max_path_len:
                        path_back.append(current)
                        current = parent[current]
                    path_back.append(current)
                    solution_path = list(reversed(path_back))
                    time_us = (time.perf_counter() - start) * 1_000_000
                    return maze, visit_order, solution_path, time_us

    time_us = (time.perf_counter() - start) * 1_000_000
    return maze, visit_order, [], time_us
