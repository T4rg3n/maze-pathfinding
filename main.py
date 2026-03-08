from maze import mazegen
import time
from dfs import dfs
from bfs import bfs
from astar import astar
from animation import run_animation, print_maze_colored

def run_pathfinding(algorithm: int) -> None:
    """Runs the chosen algorithm and prints the time it took to complete."""
    maze = mazegen()

    match algorithm:
        case 1: # DFS
            start_time = time.time()
            maze, visit_order, solution_path = dfs(maze)
            end_time = time.time()
            time_ms = (end_time - start_time) * 1000
            clear_terminal()

            # Print the maze with the visited path "p"
            maze_visited = [list(row) for row in maze]
            for r, c in visit_order:
                if maze_visited[r][c] not in ("S", "G"):
                    maze_visited[r][c] = "p"
            print("Maze with visited path: \n")
            print_maze_colored(maze_visited)
            print("\n Press any key to visualize the maze with solution path")
            clear_terminal(pause_first=True)

            # Print the maze with the solution "*"
            maze_solution = [list(row) for row in maze]
            for r, c in solution_path:
                if maze_solution[r][c] not in ("S", "G"):
                    maze_solution[r][c] = "*"
            print("Maze with solution path:")
            print_maze_colored(maze_solution)
            
            print("Press any key to visualize the solution path")
            clear_terminal(pause_first=True)

            # Print the coords of the solution path like (x, y) -> (x, y) -> (x, y)
            if solution_path:
                coords_str = " -> ".join(f"({r}, {c})" for r, c in solution_path)
                print(coords_str)
            else:
                print("No solution path.")

            path_len = len(solution_path) - 1 if solution_path else 0
            stats_box("Depth First Search", time_ms, len(visit_order), path_len)
            # At the end run the animation (after user confirmed they has seen the results)
            print("Press any key to visualize the execution animation")
            clear_terminal(pause_first=True)
            run_animation(maze, visit_order)
        case 2:
            start_time = time.time()
            bfs(maze)
            end_time = time.time()
            print(f"BFS time: {end_time - start_time} seconds")
        case 3:
            start_time = time.time()
            astar(maze)
            end_time = time.time()
            print(f"A* time: {end_time - start_time} seconds")
        case 4:
            print("Will generate a CSV containing algorithms at some point")
        case _:
            raise ValueError(f"Invalid choice: {algorithm}")


def clear_terminal(pause_first: bool = False) -> None:
    """Clear the terminal."""
    if pause_first:
        input()
    print("\033[2J\033[H", end="")

def stats_box(algorithm: str, time_ms: float, nodes_visited: int, path_length: int) -> None:
    """Print the stats in a box."""
    print(f"╔══════════════════════════════{algorithm}══════════════════════════════╗")
    print(f"║ Execution time : {time_ms:.2f} ms                       ║")
    print(f"║ Nodes visited  : {nodes_visited}                        ║")
    print(f"║ Path length    : {path_length}                          ║")
    print("╚══════════════════════════════════════════════════════╝")

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
