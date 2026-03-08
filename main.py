from maze import mazegen
import time
from dfs import dfs
from bfs import bfs
from astar import astar
from animation import run_animation, visited_frames_from_order

def print_maze(maze: list[list[str]]) -> None:
    """Print the maze to the console with spaces between cells."""
    for row in maze:
        print(' '.join(row))


def run_pathfinding(algorithm: int) -> None:
    """Generate and display a maze.

    The ``choice`` parameter is reserved for future pathfinding implementations
    (DFS, BFS, A*) that will each solve the maze differently.
    """
    maze = mazegen()

    match algorithm:
        case 1:
            start_time = time.time()
            result = dfs(maze)
            maze, visit_order = result
            end_time = time.time()
            print(f"DFS time: {end_time - start_time} seconds")
            frames = visited_frames_from_order(visit_order)
            if frames:
                run_animation(maze, frames)
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
    print()
    print_maze(maze)


def main() -> None:
    """Display the algorithm selection menu and run the chosen option."""
    menu = {
        1: 'DFS (Depth First Search)',
        2: 'BFS (Breadth First Search)',
        3: 'A*',
        4: 'Benchmark (outputs CSV)',
    }

    while True:
        print('\nSelect a pathfinding algorithm:')
        for key, name in menu.items():
            print(f'  {key}. {name}')

        choice = input('Enter your choice (1-3): ').strip()
        if choice in ('1', '2', '3', '4'):
            run_pathfinding(int(choice))
            break

        print('Invalid choice. Please enter 1, 2, or 3.')


if __name__ == '__main__':
    main()
