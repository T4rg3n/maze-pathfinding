import heapq
import time


def astar(maze: list[list[str]]) -> tuple[list[list[str]], list[tuple[int, int]], list[tuple[int, int]], float]:
    """
    A* algorithm to solve the maze.

    Informed search using a priority queue. Evaluation: f(n) = g(n) + h(n)
    with g(n) = cost from start to n, h(n) = Manhattan distance to goal.
    Returns (maze, visit_order, solution_path, time_us).
    """
    start = time.perf_counter()
    visit_order: list[tuple[int, int]] = []
    parent: dict[tuple[int, int], tuple[int, int]] = {}
    g: dict[tuple[int, int], int] = {}
    closed: set[tuple[int, int]] = set()

    # Find start and goal
    start_pos = None
    goal_pos = None
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == "S":
                start_pos = (row, col)
            if maze[row][col] == "G":
                goal_pos = (row, col)
        if start_pos is not None and goal_pos is not None:
            break

    if start_pos is None or goal_pos is None:
        time_us = (time.perf_counter() - start) * 1_000_000
        return maze, visit_order, [], time_us

    goal_row, goal_col = goal_pos
    rows = len(maze)
    cols = len(maze[0])

    def manhattan(r: int, c: int) -> int:
        return abs(r - goal_row) + abs(c - goal_col)

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    tiebreaker = 0
    g[start_pos] = 0
    f_start = g[start_pos] + manhattan(*start_pos)
    heap: list[tuple[int, int, int, tuple[int, int]]] = []
    heapq.heappush(heap, (f_start, tiebreaker, start_pos[0], start_pos[1]))
    tiebreaker += 1

    while heap:
        _, _, r, c = heapq.heappop(heap)
        node = (r, c)
        if node in closed:
            continue
        closed.add(node)
        visit_order.append(node)

        if node == goal_pos:
            path_back: list[tuple[int, int]] = []
            current = node
            max_path_len = rows * cols
            while current in parent and len(path_back) < max_path_len:
                path_back.append(current)
                current = parent[current]
            path_back.append(current)
            solution_path = list(reversed(path_back))
            time_us = (time.perf_counter() - start) * 1_000_000
            return maze, visit_order, solution_path, time_us

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            cell = maze[nr][nc]
            if cell != "." and cell != "G":
                continue
            neighbor = (nr, nc)
            tentative_g = g[node] + 1
            if neighbor not in g or tentative_g < g[neighbor]:
                g[neighbor] = tentative_g
                parent[neighbor] = node
                f = tentative_g + manhattan(nr, nc)
                heapq.heappush(heap, (f, tiebreaker, nr, nc))
                tiebreaker += 1

    time_us = (time.perf_counter() - start) * 1_000_000
    return maze, visit_order, [], time_us
