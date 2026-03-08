# maze-pathfinding

A Python console application that generates mazes and lets you choose a pathfinding algorithm to solve them.

You can chose between two modes :
- Visualization : Step by step visualization of the pathfinding process
- Benchmark : Run each algorithm 100 times and compare their performance.

## File tree

```
maze-pathfinding/
├── animation.py      # Vibe-coded animation helper to visualize algorithms pathfinding
├── main.py           # Entry point – displays the algorithm selection menu
├── mazegen.py        # Maze generator using a DFS recursive backtracker
├── requirements.txt  # Third-party dependencies (none – standard library only)
└── README.md         # This file
```

## Requirements

- Python 3.10+
- No third-party libraries required