"""
(Optional) console animation for stepping through pathfinding algorithm progress.

Takes a maze and a sequence of visited cells (or frames), and lets the user
scroll through them with simple key commands.

Controls:
  - a: previous step
  - d: next step
  - s: first step
  - e: last step
  - Enter: skip to end and exit
  - q: quit to summary
"""

import os

# ANSI foreground colors (basic)
_RED = "\033[31m"
_GREEN = "\033[32m"
_WHITE = "\033[37m"
_GRAY = "\033[90m"
_LIGHT_GRAY = "\033[97m"
_RESET = "\033[0m"
_YELLOW = "\033[33m"
_BLUE = "\033[34m"

# 256-color yellow/gold gradient (dark → bright)
_YELLOW_GRADIENT = [220, 221, 222, 223, 224, 226]


def _color_for_visit_age(first_step: int, max_step: int) -> str:
    """Return a 256-color ANSI code representing the age of a visited cell."""
    if max_step <= 0:
        index = len(_YELLOW_GRADIENT) - 1
    else:
        ratio = first_step / max_step
        index = int(ratio * (len(_YELLOW_GRADIENT) - 1))
    index = max(0, min(index, len(_YELLOW_GRADIENT) - 1))
    color_code = _YELLOW_GRADIENT[index]
    return f"\033[38;5;{color_code}m"


def _colorize_cell(char: str) -> str:
    """Return the cell character wrapped in ANSI color codes."""
    if char == "S":
        return f"{_RED}S{_RESET}"
    if char == "G":
        return f"{_GREEN}G{_RESET}"
    if char == "#":
        return f"{_WHITE}#{_RESET}"
    if char == ".":
        return f"{_GRAY}.{_RESET}"
    return char


def _render_maze(
    maze: list[list[str]],
    visited: set[tuple[int, int]],
    visited_char: str = "x",
) -> list[list[str]]:
    """Build a copy of the maze with visited cells marked."""
    rows, cols = len(maze), len(maze[0])
    out = [list(row) for row in maze]
    for r, c in visited:
        if 0 <= r < rows and 0 <= c < cols:
            cell = out[r][c]
            if cell not in ("S", "G"):
                out[r][c] = visited_char
    return out


def _print_frame(
    maze: list[list[str]],
    step: int,
    total: int,
    first_visit: dict[tuple[int, int], int],
    max_step: int,
    title: str | None = None,
) -> None:
    """Print the maze and step indicator to the console with colors."""
    # Clear screen and move cursor home (works on Windows and most terminals)
    print("\033[2J\033[H", end="")
    if title:
        print(title)
        print()
    for r, row in enumerate(maze):
        rendered_row: list[str] = []
        for c, ch in enumerate(row):
            if ch == "x":
                idx = first_visit.get((r, c))
                if idx is not None:
                    color = _color_for_visit_age(idx, max_step)
                    rendered_row.append(f"{color}x{_RESET}")
                else:
                    rendered_row.append(_colorize_cell("x"))
            else:
                rendered_row.append(_colorize_cell(ch))
        print(" ".join(rendered_row))
    print()
    print(f"Step {step + 1} / {total}  (a: prev  d: next  s: first  e: last  Enter: skip  q: quit)")


def _read_key() -> str:
    """Read a single key command.

    On Windows this uses ``msvcrt.getch`` for instant keypresses.
    On other platforms it falls back to ``input()``, which requires Enter.
    """
    if os.name == "nt":
        try:
            import msvcrt
        except ImportError:
            cmd = input().strip().lower()
            return cmd[0] if cmd else ""

        ch = msvcrt.getch()
        if ch in (b"q", b"Q"):
            return "q"
        if ch in (b"\r", b"\n"):
            return "enter"
        try:
            return ch.decode(errors="ignore").lower()
        except Exception:
            return ""

    # Non-Windows: simple line-based input (Enter alone returns "enter")
    cmd = input().strip().lower()
    if not cmd:
        return "enter"
    return cmd[0]


def run_animation(
    maze: list[list[str]],
    visit_order: list[tuple[int, int]],
    visited_char: str = "x",
    title: str | None = None,
) -> None:
    """Display the maze and let the user scroll through visited cells with key commands.

    Args:
        maze: 2D grid of strings ('#', '.', 'S', 'G').
        visit_order: Ordered list of (row, col) pairs giving the order in which
            the algorithm visited cells.
        visited_char: Character used to mark visited cells (default 'x').
        title: Optional title shown above the maze (e.g. "Maze with exploration animation").
    """
    # Build cumulative visited sets for each step, starting with an empty frame,
    # and record the first step at which each cell was visited.
    visited_frames: list[set[tuple[int, int]]] = [set()]
    current: set[tuple[int, int]] = set()
    first_visit: dict[tuple[int, int], int] = {}
    for idx, cell in enumerate(visit_order):
        current = current | {cell}
        visited_frames.append(current.copy())
        if cell not in first_visit:
            first_visit[cell] = idx

    if not visited_frames:
        visited_frames = [set()]

    max_step = len(visit_order) - 1 if visit_order else 0
    total = len(visited_frames)
    step = 0

    while True:
        visited = visited_frames[step]
        display = _render_maze(maze, visited, visited_char=visited_char)
        _print_frame(display, step, total, first_visit, max_step, title=title)

        key = _read_key()
        if not key:
            continue

        if key == "q":
            break
        if key == "enter":
            step = total - 1
            visited = visited_frames[step]
            display = _render_maze(maze, visited, visited_char=visited_char)
            _print_frame(display, step, total, first_visit, max_step, title=title)
            break
        if key == "a" and step > 0:
            step -= 1
        if key == "d" and step < total - 1:
            step += 1
        if key == "s":
            step = 0
        if key == "e":
            step = total - 1

def print_maze_colored(maze: list[list[str]]) -> None:
    """Print the maze with colored cells :
    p -> yellow
    * -> blue
    x -> gray
    S -> red
    G -> green
    # -> white
    . -> gray
    """
    for row in maze:
        for cell in row:
            match cell:
                case "p":
                    print(f"{_YELLOW}{cell}{_RESET}", end=" ")
                case "x":
                    print(f"{_GRAY}{cell}{_RESET}", end=" ")
                case "S":
                    print(f"{_RED}{cell}{_RESET}", end=" ")
                case "G":
                    print(f"{_GREEN}{cell}{_RESET}", end=" ")
                case "#":
                    print(f"{_WHITE}{cell}{_RESET}", end=" ")
                case ".":
                    print(f"{_GRAY}{cell}{_RESET}", end=" ")
                case "*":
                    print(f"{_BLUE}{cell}{_RESET}", end=" ")
                case _:
                    print(cell, end=" ")
        print()