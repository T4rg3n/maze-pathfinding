"""
Benchmark runner: 100 different mazes, 1 run per algorithm per maze (300 runs total).
Executes DFS, BFS, and A* on each maze, records metrics, computes IQR-based statistics,
and writes a single CSV with summary at top and raw data below.
"""
import csv
import os
import statistics
import sys
import tracemalloc

# Run from project root so imports work
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from maze import mazegen
from dfs import dfs
from bfs import bfs
from astar import astar


NUM_MAZES = 100
SEEDS = range(42, 42 + NUM_MAZES)
METRICS = ("time_us", "memory_kb", "nodes_explored", "path_length")


def copy_maze(maze: list[list[str]]) -> list[list[str]]:
    return [row[:] for row in maze]


def run_one(algorithm_name: str, maze: list[list[str]]) -> tuple[float, float, int, int]:
    """Run algorithm once; return (time_us, memory_kb, nodes_explored, path_length)."""
    maze_copy = copy_maze(maze)
    tracemalloc.start()
    if algorithm_name == "DFS":
        _, visit_order, solution_path, time_us = dfs(maze_copy)
    elif algorithm_name == "BFS":
        _, visit_order, solution_path, time_us = bfs(maze_copy)
    else:  # A*
        _, visit_order, solution_path, time_us = astar(maze_copy)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    memory_kb = peak / 1024.0
    nodes_explored = len(visit_order)
    path_length = len(solution_path) - 1 if solution_path else 0
    return (time_us, memory_kb, nodes_explored, path_length)


def iqr_stats(values: list[float]) -> dict[str, float]:
    """Compute n, median, q1, q3, iqr, mean, std. Uses statistics.quantiles for Q1/Q3."""
    n = len(values)
    if n == 0:
        return {"n": 0, "median": 0, "q1": 0, "q3": 0, "iqr": 0, "mean": 0, "std": 0}
    q = statistics.quantiles(values, n=4)
    q1, q3 = q[0], q[2]
    return {
        "n": n,
        "median": statistics.median(values),
        "q1": q1,
        "q3": q3,
        "iqr": q3 - q1,
        "mean": statistics.mean(values),
        "std": statistics.stdev(values) if n > 1 else 0.0,
    }


def run_benchmarks() -> None:
    csv_dir = os.path.dirname(__file__)
    csv_path = os.path.join(csv_dir, "benchmark.csv")

    algorithms = [
        ("DFS", dfs),
        ("BFS", bfs),
        ("A*", astar),
    ]

    # Collect raw runs: list of (algorithm, seed, time_us, memory_kb, nodes_explored, path_length)
    raw_rows: list[tuple[str, int, float, float, int, int]] = []
    for seed in SEEDS:
        maze = mazegen(seed=seed)
        for alg_name, _ in algorithms:
            time_us, memory_kb, nodes_explored, path_length = run_one(alg_name, maze)
            raw_rows.append((alg_name, seed, time_us, memory_kb, nodes_explored, path_length))

    # Build summary: for each (algorithm, metric) compute IQR stats
    summary_rows: list[dict] = []
    for alg_name, _ in algorithms:
        alg_runs = [(t, m, n, p) for a, _, t, m, n, p in raw_rows if a == alg_name]
        time_vals = [r[0] for r in alg_runs]
        memory_vals = [r[1] for r in alg_runs]
        nodes_vals = [float(r[2]) for r in alg_runs]
        path_vals = [float(r[3]) for r in alg_runs]
        for metric, values in [
            ("time_us", time_vals),
            ("memory_kb", memory_vals),
            ("nodes_explored", nodes_vals),
            ("path_length", path_vals),
        ]:
            s = iqr_stats(values)
            summary_rows.append({
                "algorithm": alg_name,
                "metric": metric,
                "n": s["n"],
                "median": s["median"],
                "q1": s["q1"],
                "q3": s["q3"],
                "iqr": s["iqr"],
                "mean": s["mean"],
                "std": s["std"],
            })

    # Write single CSV: summary at top, then raw data below
    summary_fieldnames = ["algorithm", "metric", "n", "median", "q1", "q3", "iqr", "mean", "std"]
    raw_fieldnames = ["run_id", "algorithm", "seed", "time_us", "memory_kb", "nodes_explored", "path_length"]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(summary_fieldnames)
        for row in summary_rows:
            w.writerow([row[k] for k in summary_fieldnames])
        w.writerow([])  # separator
        w.writerow(raw_fieldnames)
        for i, (alg_name, seed, time_us, memory_kb, nodes_explored, path_length) in enumerate(raw_rows):
            w.writerow([i, alg_name, seed, time_us, memory_kb, nodes_explored, path_length])

    # Print results table to console
    print(f"\nBenchmark complete. Results written to {csv_path}\n")
    print(f"{'algorithm':<10} {'nodes':>8} {'length':>8} {'time_ms':>10}")
    print("-" * 38)
    for alg_name, _ in algorithms:
        rows = [r for r in summary_rows if r["algorithm"] == alg_name]
        nodes = int(next((r["median"] for r in rows if r["metric"] == "nodes_explored"), 0))
        length = int(next((r["median"] for r in rows if r["metric"] == "path_length"), 0))
        time_us = next((r["median"] for r in rows if r["metric"] == "time_us"), 0)
        time_ms = time_us / 1000.0
        print(f"{alg_name:<10} {nodes:>8} {length:>8} {time_ms:>10.3f}")


if __name__ == "__main__":
    run_benchmarks()
