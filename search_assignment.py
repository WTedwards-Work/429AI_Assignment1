from collections import deque
from typing import Dict, List, Tuple, Optional, Set

Node = str
PathNodes = List[Node]
Coord = Tuple[int, int]
PathCoords = List[Coord]


# ----------------------------
# Problem 1(a,b): Graph Search
# ----------------------------

GRAPH: Dict[Node, List[Node]] = {
    "A": ["B"],
    "B": ["C", "D"],
    "C": ["E"],
    "D": ["F"],
    "E": [],
    "F": [],
}

GRAPH_START: Node = "A"
GRAPH_GOAL: Node = "E"


def bfs_graph(graph: Dict[Node, List[Node]], start: Node, goal: Node) -> Optional[PathNodes]:
    """BFS on a directed graph. Returns shortest path (by edges) if reachable """
    q = deque([(start, [start])])
    visited: Set[Node] = set()

    while q:
        node, path = q.popleft()
        if node == goal:
            return path
        if node in visited:
            continue
        visited.add(node)
        for nbr in graph.get(node, []):
            if nbr not in visited:
                q.append((nbr, path + [nbr]))
    return None


def dfs_graph(graph: Dict[Node, List[Node]], start: Node, goal: Node) -> Optional[PathNodes]:
    """DFS on a directed graph. Returns a path if reachable (not guaranteed shortest)."""
    stack = [(start, [start])]
    visited: Set[Node] = set()

    while stack:
        node, path = stack.pop()
        if node == goal:
            return path
        if node in visited:
            continue
        visited.add(node)

        # reverse so the left-most neighbor is explored first when pooped
        for nbr in reversed(graph.get(node, [])):
            if nbr not in visited:
                stack.append((nbr, path + [nbr]))
    return None


# ---------------------------------------
# Problem 1(c,d) + Problem 2: Grid Search
# ---------------------------------------

# 7 rows x 6 cols
# 0 = free (black), 1 = blocked (gray)
GRID: List[List[int]] = [
    [0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 1],
    [0, 1, 1, 0, 1, 1],  # B is at (3,3)
    [0, 1, 0, 0, 1, 1],
    [0, 1, 0, 1, 1, 1],
    [0, 0, 0, 1, 1, 1],  # A is at (6,0)
]

GRID_START: Coord = (6, 0)  # A
GRID_GOAL: Coord = (3, 3)   # B

# neighbors order matters for DFS/DLS paths
# using Right, Down, Left, Up
DIRS: List[Tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def in_bounds(grid: List[List[int]], r: int, c: int) -> bool:
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


def is_free(grid: List[List[int]], r: int, c: int) -> bool:
    return grid[r][c] == 0


def bfs_grid(grid: List[List[int]], start: Coord, goal: Coord) -> Optional[PathCoords]:
    """BFS on a grid. Returns shortest path (by moves) if reachable """
    q = deque([(start, [start])])
    visited: Set[Coord] = set()

    while q:
        (r, c), path = q.popleft()
        if (r, c) == goal:
            return path
        if (r, c) in visited:
            continue
        visited.add((r, c))

        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if in_bounds(grid, nr, nc) and is_free(grid, nr, nc) and (nr, nc) not in visited:
                q.append(((nr, nc), path + [(nr, nc)]))
    return None


def dfs_grid(grid: List[List[int]], start: Coord, goal: Coord) -> Optional[PathCoords]:
    """DFS on a grid. Returns a path if reachable (not guaranteed shortest) """
    stack = [(start, [start])]
    visited: Set[Coord] = set()

    while stack:
        (r, c), path = stack.pop()
        if (r, c) == goal:
            return path
        if (r, c) in visited:
            continue
        visited.add((r, c))

        for dr, dc in reversed(DIRS):
            nr, nc = r + dr, c + dc
            if in_bounds(grid, nr, nc) and is_free(grid, nr, nc) and (nr, nc) not in visited:
                stack.append(((nr, nc), path + [(nr, nc)]))
    return None


def dls_grid(
    grid: List[List[int]],
    start: Coord,
    goal: Coord,
    limit: int,
) -> Tuple[Optional[PathCoords], int]:
    """
    Depth-Limited Search on a grid (DFS with a depth cutoff)
    Returns (path or None, expansions_count).

    expansions_count = number of times we expanded a node (generated neighbors)
    """
    stack = [(start, [start], 0)]  # (node, path, depth)
    expansions = 0

    while stack:
        (r, c), path, depth = stack.pop()

        if (r, c) == goal:
            return path, expansions

        if depth == limit:
            continue

        expansions += 1

        for dr, dc in reversed(DIRS):
            nr, nc = r + dr, c + dc
            if in_bounds(grid, nr, nc) and is_free(grid, nr, nc):
                # avoid cycles on the current path
                if (nr, nc) not in path:
                    stack.append(((nr, nc), path + [(nr, nc)], depth + 1))

    return None, expansions


# ------------------------
# Pretty printing helpers!
# ------------------------

def print_path_nodes(label: str, path: Optional[PathNodes]) -> None:
    print(label)
    if path is None:
        print("  No path found.")
    else:
        print(" ", path)
        print("  Path length (edges):", len(path) - 1)


def print_path_coords(label: str, path: Optional[PathCoords]) -> None:
    print(label)
    if path is None:
        print("  No path found.")
    else:
        print(" ", path)
        print("  Path length (moves):", len(path) - 1)


# --------
# Runners 
# --------

def run_problem_1() -> None:
    print("===== PROBLEM 1 =====")

    # (a) BFS on graph
    bfs_g = bfs_graph(GRAPH, GRAPH_START, GRAPH_GOAL)
    print_path_nodes("1(a) BFS graph A → E:", bfs_g)

    # (b) DFS on graph
    dfs_g = dfs_graph(GRAPH, GRAPH_START, GRAPH_GOAL)
    print_path_nodes("1(b) DFS graph A → E:", dfs_g)

    # (c) BFS on grid
    bfs_p = bfs_grid(GRID, GRID_START, GRID_GOAL)
    print_path_coords("1(c) BFS grid A → B:", bfs_p)

    # (d) DFS on grid
    dfs_p = dfs_grid(GRID, GRID_START, GRID_GOAL)
    print_path_coords("1(d) DFS grid A → B:", dfs_p)


def run_problem_2() -> None:
    print("\n===== PROBLEM 2 =====")
    print("Depth-Limited Search (DLS) on grid A → B")

    for lim in (4, 8):
        path, expansions = dls_grid(GRID, GRID_START, GRID_GOAL, lim)
        print(f"\nDLS limit = {lim}")
        print("Expansions:", expansions)
        if path is None:
            print("No path found within depth limit.")
        else:
            print("Found path:", path)
            print("Path length (moves):", len(path) - 1)


def run_all() -> None:
    print("Search Algorithms Assignment")
    print("------------------------------------------------")
    run_problem_1()
    run_problem_2()


if __name__ == "__main__":
    run_all()
