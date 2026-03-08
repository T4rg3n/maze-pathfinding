from mazegen import mazegen

from dfs import dfs
from bfs import bfs
from astar import astar

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
            dfs(maze)
        case 2:
            bfs(maze)
        case 3:
            astar(maze)
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
    }

    while True:
        print('\nSelect a pathfinding algorithm:')
        for key, name in menu.items():
            print(f'  {key}. {name}')

        choice = input('Enter your choice (1-3): ').strip()
        if choice in ('1', '2', '3'):
            run_pathfinding(int(choice))
            break

        print('Invalid choice. Please enter 1, 2, or 3.')


if __name__ == '__main__':
    main()
