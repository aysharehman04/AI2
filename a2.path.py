# a2_path.py
"""
Group ID:
Student ID:

Task 2 – Safe Path Search for the Hinger Game

This module implements the following algorithms:
  - path_BFS
  - path_DFS
  - path_IDDFS
  - path_astar
  - compare()
  - tester()

Each function works only with the State class defined in a1_state.py.
No external Python libraries are used (other than importing State).
"""

from a1_state import State


# =====================================================
# Helper functions
# =====================================================
def grid_to_key(grid):
    """Turn a grid into a tuple-of-tuples so it can be compared easily."""
    return tuple(tuple(row) for row in grid)


def states_equal(s1, s2):
    """Return True if two states have identical grids."""
    return s1.grid == s2.grid


def is_safe(state):
    """Return True if a state is safe (contains no hingers)."""
    return state.numHingers() == 0


def move_cost_between(s1, s2):
    """Find which cell changed and return s1.move_cost(r, c)."""
    for r in range(s1.rows):
        for c in range(s1.cols):
            if s1.grid[r][c] - s2.grid[r][c] == 1:
                return s1.move_cost(r, c)
    return 0


def path_cost(path):
    """Compute total cost along a path (list of States)."""
    total = 0
    for i in range(len(path) - 1):
        total += move_cost_between(path[i], path[i + 1])
    return total


# =====================================================
# Breadth-First Search
# =====================================================
def path_BFS(start, end):
    """Breadth-First Search to find a safe path between start and end."""
    if not is_safe(start) or not is_safe(end):
        return None
    if states_equal(start, end):
        return [start]

    frontier = [(start, [start])]
    visited = [grid_to_key(start.grid)]

    while frontier:
        current, path = frontier.pop(0)
        for next_state, pos, cost in current.moves():
            key = grid_to_key(next_state.grid)
            if key in visited:
                continue
            if not is_safe(next_state):
                continue
            visited.append(key)
            new_path = path + [next_state]
            if states_equal(next_state, end):
                return new_path
            frontier.append((next_state, new_path))
    return None


# =====================================================
# Depth-First Search
# =====================================================
def path_DFS(start, end, limit=10000):
    """Depth-First Search using a stack (no recursion)."""
    if not is_safe(start) or not is_safe(end):
        return None
    if states_equal(start, end):
        return [start]

    stack = [(start, [start])]
    visited = [grid_to_key(start.grid)]

    steps = 0
    while stack:
        current, path = stack.pop()
        steps += 1
        if steps > limit:
            return None
        for next_state, pos, cost in current.moves():
            key = grid_to_key(next_state.grid)
            if key in visited:
                continue
            if not is_safe(next_state):
                continue
            visited.append(key)
            new_path = path + [next_state]
            if states_equal(next_state, end):
                return new_path
            stack.append((next_state, new_path))
    return None


# =====================================================
# Iterative Deepening DFS
# =====================================================
def _limited_dfs(current, end, depth, visited):
    """Recursive helper for depth-limited search."""
    if states_equal(current, end):
        return [current]
    if depth == 0:
        return None
    for next_state, pos, cost in current.moves():
        key = grid_to_key(next_state.grid)
        if key in visited or not is_safe(next_state):
            continue
        visited.append(key)
        result = _limited_dfs(next_state, end, depth - 1, visited)
        visited.pop()
        if result:
            return [current] + result
    return None


def path_IDDFS(start, end, max_depth=20):
    """Iterative Deepening DFS."""
    if not is_safe(start) or not is_safe(end):
        return None
    if states_equal(start, end):
        return [start]

    for depth in range(1, max_depth + 1):
        visited = [grid_to_key(start.grid)]
        result = _limited_dfs(start, end, depth, visited)
        if result:
            return result
    return None


# =====================================================
# A* Search (Manhattan heuristic)
# =====================================================
def manhattan_heuristic(start, end):
    """
    Compute Manhattan-style heuristic between two binary grids.
    It sums the distances between '1' cells (active cells) after
    sorting them in row-major order. Admissible but simple.
    """
    s1 = []
    s2 = []
    for r in range(start.rows):
        for c in range(start.cols):
            if start.grid[r][c] == 1:
                s1.append((r, c))
            if end.grid[r][c] == 1:
                s2.append((r, c))

    s1.sort()
    s2.sort()

    total = 0
    length = min(len(s1), len(s2))
    for i in range(length):
        r1, c1 = s1[i]
        r2, c2 = s2[i]
        total += abs(r1 - r2) + abs(c1 - c2)

    total += abs(len(s1) - len(s2))
    return total


def path_astar(start, end):
    """A* Search using Manhattan-style heuristic."""
    if not is_safe(start) or not is_safe(end):
        return None
    if states_equal(start, end):
        return [start]

    open_list = [start]
    came_from = {}
    g = {grid_to_key(start.grid): 0}
    f = {grid_to_key(start.grid): manhattan_heuristic(start, end)}
    closed = []

    while open_list:
        current = open_list[0]
        best_f = f[grid_to_key(current.grid)]
        for s in open_list:
            key = grid_to_key(s.grid)
            if f[key] < best_f:
                current = s
                best_f = f[key]

        open_list.remove(current)
        closed.append(grid_to_key(current.grid))

        if states_equal(current, end):
            path = [current]
            key = grid_to_key(current.grid)
            while key in came_from:
                key = came_from[key]
                prev_grid = [list(r) for r in key]
                prev_state = State(prev_grid)
                path.insert(0, prev_state)
            return path

        for next_state, pos, cost in current.moves():
            key_next = grid_to_key(next_state.grid)
            if key_next in closed or not is_safe(next_state):
                continue

            g_new = g[grid_to_key(current.grid)] + cost
            if (key_next not in g) or (g_new < g[key_next]):
                came_from[key_next] = grid_to_key(current.grid)
                g[key_next] = g_new
                f[key_next] = g_new + manhattan_heuristic(next_state, end)
                in_open = False
                for s in open_list:
                    if grid_to_key(s.grid) == key_next:
                        in_open = True
                        break
                if not in_open:
                    open_list.append(next_state)
    return None


# =====================================================
# Compare algorithms
# =====================================================
def compare(start, end):
    """Print comparison results for BFS, DFS, IDDFS, and A*."""
    print("\nComparing search algorithms:\n")
    algos = [
        ("BFS", path_BFS),
        ("DFS", path_DFS),
        ("IDDFS", path_IDDFS),
        ("A*", path_astar)
    ]

    for name, func in algos:
        path = func(start, end)
        if path:
            print(f"{name:6} | Success | Path length: {len(path)} | Total cost: {path_cost(path)}")
        else:
            print(f"{name:6} | Failed to find a path.")


# =====================================================
# Tester
# =====================================================
def tester():
    """Simple tester to validate search functions."""
    print("=== a2_path.py tester ===")

    g = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]
    s = State(g)
    e = State(g)

    print("Trivial test (start == end):")
    compare(s, e)

    print("\nExample for manual testing:")
    print("from a1_state import State")
    print("from a2_path import path_BFS, compare")
    print("start = State([[1,1,0],[0,1,0],[0,0,0]])")
    print("end   = State([[0,1,1],[0,0,1],[0,0,0]])")
    print("compare(start, end)")


if __name__ == "__main__":
    tester()
