from maze import mazegen
from dfs import dfs
from bfs import bfs
from astar import astar
from animation import run_animation, print_maze_colored

def run_pathfinding(algorithm: int) -> None:
    """Runs the chosen algorithm and prints the time it took to complete."""
    maze = mazegen()

    match algorithm:
        case 1: # DFS
            maze, visit_order, solution_path, time_us = dfs(maze)
            clear_terminal()

            # Print the maze with the visited path "p"
            maze_visited = [list(row) for row in maze]
            for r, c in visit_order:
                if maze_visited[r][c] not in ("S", "G"):
                    maze_visited[r][c] = "p"
            print("(1/4) Maze with visited path: \n")
            print_maze_colored(maze_visited)
            print("\n Press any key to visualize the maze with solution path")
            clear_terminal(pause_first=True)

            # Print the maze with the solution "*"
            maze_solution = [list(row) for row in maze]
            for r, c in solution_path:
                if maze_solution[r][c] not in ("S", "G"):
                    maze_solution[r][c] = "*"
            print("(2/4) Maze with solution path:")
            print_maze_colored(maze_solution)
            
            print("Press any key to visualize the solution path")
            clear_terminal(pause_first=True)

            # Print the coords of the solution path like (x, y) -> (x, y) -> (x, y)
            print("(3/4) Solution path:")
            if solution_path:
                coords_str = " -> ".join(f"({r}, {c})" for r, c in solution_path)
                print(coords_str)
            else:
                print("No solution path.")

            path_len = len(solution_path) - 1 if solution_path else 0
            stats_box("Depth First Search", time_us, len(visit_order), path_len)
            # At the end run the animation (exploration order, not solution path)
            print("Press any key to visualize the exploration animation")
            clear_terminal(pause_first=True)
            run_animation(maze, visit_order, title="(4/4) Maze with exploration animation")
        case 2:  # BFS
            maze, visit_order, solution_path, time_us = bfs(maze)
            clear_terminal()

            # Print the maze with the visited path "p"
            maze_visited = [list(row) for row in maze]
            for r, c in visit_order:
                if maze_visited[r][c] not in ("S", "G"):
                    maze_visited[r][c] = "p"
            print("(1/4) Maze with visited path: \n")
            print_maze_colored(maze_visited)
            print("\n Press any key to visualize the maze with solution path")
            clear_terminal(pause_first=True)

            # Print the maze with the solution "*"
            maze_solution = [list(row) for row in maze]
            for r, c in solution_path:
                if maze_solution[r][c] not in ("S", "G"):
                    maze_solution[r][c] = "*"
            print("(2/4) Maze with solution path:")
            print_maze_colored(maze_solution)
            print("\n Press any key to visualize the solution path")
            clear_terminal(pause_first=True)

            print("(3/4) Solution path:")
            if solution_path:
                coords_str = " -> ".join(f"({r}, {c})" for r, c in solution_path)
                print(coords_str)
            else:
                print("No solution path.")

            path_len = len(solution_path) - 1 if solution_path else 0
            stats_box("Breadth First Search", time_us, len(visit_order), path_len)
            print("Press any key to visualize the exploration animation")
            clear_terminal(pause_first=True)
            run_animation(maze, visit_order, title="(4/4) Maze with exploration animation")
        case 3:  # A*
            maze, visit_order, solution_path, time_us = astar(maze)
            clear_terminal()

            maze_visited = [list(row) for row in maze]
            for r, c in visit_order:
                if maze_visited[r][c] not in ("S", "G"):
                    maze_visited[r][c] = "p"
            print("(1/4) Maze with visited path: \n")
            print_maze_colored(maze_visited)
            print("\n Press any key to visualize the maze with solution path")
            clear_terminal(pause_first=True)

            maze_solution = [list(row) for row in maze]
            for r, c in solution_path:
                if maze_solution[r][c] not in ("S", "G"):
                    maze_solution[r][c] = "*"
            print("(2/4) Maze with solution path:")
            print_maze_colored(maze_solution)
            print("\n Press any key to visualize the solution path")
            clear_terminal(pause_first=True)

            print("(3/4) Solution path:")
            if solution_path:
                coords_str = " -> ".join(f"({r}, {c})" for r, c in solution_path)
                print(coords_str)
            else:
                print("No solution path.")

            path_len = len(solution_path) - 1 if solution_path else 0
            stats_box("A*", time_us, len(visit_order), path_len)
            print("Press any key to visualize the exploration animation")
            clear_terminal(pause_first=True)
            run_animation(maze, visit_order, title="(4/4) Maze with exploration animation")
        case 4:
            print("Will generate a CSV containing algorithms at some point")
        case _:
            raise ValueError(f"Invalid choice: {algorithm}")


def clear_terminal(pause_first: bool = False) -> None:
    """Clear the terminal."""
    if pause_first:
        input()
    print("\033[2J\033[H", end="")

def stats_box(algorithm: str, time_us: float, nodes_visited: int, path_length: int) -> None:
    """Print the stats in a box. Time is in microseconds (µs)."""
    print(f"\n╔═══════{algorithm}═══════╗")
    print(f"║ Execution time : {time_us:.1f} µs  ")
    print(f"║ Nodes visited  : {nodes_visited}")
    print(f"║ Path length    : {path_length}")
    print("╚══════════════════════════════════╝")

def main() -> None:
    """Display the algorithm selection menu and run the chosen option."""
    menu = {
        1: 'Visualize DFS (Depth First Search)',
        2: 'Visualize BFS (Breadth First Search)',
        3: 'Visualize A*',
        4: 'Benchmark all algorithms',
    }

    while True:
        print('\nSelect a pathfinding algorithm:')
        for key, name in menu.items():
            print(f'  {key}. {name}')

        choice = input('Enter your choice (1-4): ').strip()
        if choice in ('1', '2', '3', '4'):
            run_pathfinding(int(choice))
            break

        print('Invalid choice. Please enter 1, 2, or 3.')


if __name__ == '__main__':
    main()
