# maze-pathfinding

A Python console application that generates mazes and lets you choose a pathfinding algorithm to solve them.

---

## File tree

```
maze-pathfinding/
├── main.py           # Entry point – displays the algorithm selection menu
├── mazegen.py        # Maze generator using a DFS recursive backtracker
├── requirements.txt  # Third-party dependencies (none – standard library only)
└── README.md         # This file
```

---

## Getting started

### 1 – Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 2 – Install dependencies

```bash
pip install -r requirements.txt
```

### 3 – Run the application

```bash
python main.py
```

You will be presented with a menu:

```
Select a pathfinding algorithm:
  1. DFS (Depth First Search)
  2. BFS (Breadth First Search)
  3. A*
Enter your choice (1-3):
```

Select an option and a randomly generated maze will be printed to the terminal.

---

## Requirements

- Python 3.10+
- No third-party libraries required