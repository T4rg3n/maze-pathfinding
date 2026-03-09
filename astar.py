import heapq
import time


def astar(maze: list[list[str]]) -> tuple[list[list[str]], list[tuple[int, int]], list[tuple[int, int]], float]:
    """
    A* algorithm to solve the maze.

    Informed search using a priority queue. Evaluation: f(n) = g(n) + h(n)
    with g(n) = cost from start to n, h(n) = Manhattan distance to goal.
    Returns (maze, visit_order, solution_path, time_us).
    """
    start_time = time.perf_counter()

    visit_order: list[tuple[int, int]] = []
    parent: dict[tuple[int, int], tuple[int, int]] = {}
    g: dict[tuple[int, int], int] = {}
    closed: set[tuple[int, int]] = set()

    # Find start and goal
    start_pos: tuple[int, int] | None = None
    goal_pos: tuple[int, int] | None = None

    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == "S":
                start_pos = (r, c)
            elif maze[r][c] == "G":
                goal_pos = (r, c)
        if start_pos is not None and goal_pos is not None:
            break

    if start_pos is None or goal_pos is None:
        time_us = (time.perf_counter() - start_time) * 1_000_000
        return maze, visit_order, [], time_us

    goal_r, goal_c = goal_pos
    rows = len(maze)

    # Manhattan heuristic
    def manhattan(r: int, c: int) -> int:
        return abs(r - goal_r) + abs(c - goal_c)

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Priority queue entries: (f, tiebreaker, r, c)
    heap: list[tuple[int, int, int, int]] = []
    tiebreaker = 0

    g[start_pos] = 0
    f_start = manhattan(*start_pos)
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
            # Reconstruct path
            path_back: list[tuple[int, int]] = []
            current = node

            while current in parent:
                path_back.append(current)
                current = parent[current]

            path_back.append(current)
            solution_path = list(reversed(path_back))

            time_us = (time.perf_counter() - start_time) * 1_000_000
            return maze, visit_order, solution_path, time_us

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Bounds check (supports ragged rows)
            if not (0 <= nr < rows and 0 <= nc < len(maze[nr])):
                continue

            cell = maze[nr][nc]

            # Skip walls
            if cell == "#":
                continue
            neighbor = (nr, nc)
            if neighbor in closed:
                continue

            tentative_g = g[node] + 1
            if neighbor not in g or tentative_g < g[neighbor]:
                g[neighbor] = tentative_g
                parent[neighbor] = node

                f_neighbor = tentative_g + manhattan(nr, nc)
                heapq.heappush(heap, (f_neighbor, tiebreaker, nr, nc))
                tiebreaker += 1

    time_us = (time.perf_counter() - start_time) * 1_000_000
    return maze, visit_order, [], time_us
