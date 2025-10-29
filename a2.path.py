# a2_path.py
"""
Group ID: B1
Student ID: 100464246

Task 2 – Safe Path Search for the Hinger Game

This module implements the following algorithms:
  - path_BFS
  - path_DFS
  - path_IDDFS
  - path_astar
  - min_safe
  - compare()
  - tester()
"""

from a1_state import State


# =====================================================
# Helper functions
# =====================================================
def GridToKey(grid):
    """Turn a grid into a tuple so it can be hashed/compared."""
    return tuple(tuple(row) for row in grid)


def StatesEqual(s1, s2):
    """Return True if two states have identical grids."""
    return s1.grid == s2.grid


def IsSafe(state):
    """Return True if a state is safe (no hingers)."""
    return state.numHingers() == 0


def MoveCostBetween(s1, s2):
    """Find which cell changed and return the move cost."""
    for r in range(s1.rows):
        for c in range(s1.cols):
            if s1.grid[r][c] - s2.grid[r][c] == 1:
                return s1.move_cost(r, c)
    return 0


def PathCost(path):
    """Compute total cost along a path."""
    total = 0
    for i in range(len(path) - 1):
        total += MoveCostBetween(path[i], path[i + 1])
    return total


# =====================================================
# Breadth-First Search
# =====================================================
def path_BFS(start, end):
    """Breadth-First Search to find a safe path between start and end."""
    if not IsSafe(start) or not IsSafe(end):
        return None
    if StatesEqual(start, end):
        return [start]

    frontier = [(start, [start])]
    visited = {GridToKey(start.grid)}

    while frontier:
        current, path = frontier.pop(0)
        for NextState, pos, cost in current.moves():
            key = GridToKey(NextState.grid)
            if key in visited:
                continue
            if not IsSafe(NextState):
                continue
            visited.add(key)
            NewPath = path + [NextState]
            if StatesEqual(NextState, end):
                return NewPath
            frontier.append((NextState, NewPath))
    return None


# =====================================================
# Depth-First Search
# =====================================================
def path_DFS(start, end, limit=10000):
    """Depth-First Search using a stack."""
    if not IsSafe(start) or not IsSafe(end):
        return None
    if StatesEqual(start, end):
        return [start]

    stack = [(start, [start])]
    visited = {GridToKey(start.grid)}

    steps = 0
    while stack:
        current, path = stack.pop()
        steps += 1
        if steps > limit:
            return None
        for NextState, pos, cost in current.moves():
            key = GridToKey(NextState.grid)
            if key in visited:
                continue
            if not IsSafe(NextState):
                continue
            visited.add(key)
            NewPath = path + [NextState]
            if StatesEqual(NextState, end):
                return NewPath
            stack.append((NextState, NewPath))
    return None


# =====================================================
# Iterative Deepening DFS
# =====================================================
def limited_dfs(current, end, depth, visited):
    """Recursive helper for depth-limited search."""
    if StatesEqual(current, end):
        return [current]
    if depth == 0:
        return None
    for NextState, pos, cost in current.moves():
        key = GridToKey(NextState.grid)
        if key in visited or not IsSafe(NextState):
            continue
        visited.add(key)
        result = limited_dfs(NextState, end, depth - 1, visited)
        visited.remove(key)
        if result:
            return [current] + result
    return None


def path_IDDFS(start, end, MaxDepth=50):
    """Iterative Deepening DFS."""
    if not IsSafe(start) or not IsSafe(end):
        return None
    if StatesEqual(start, end):
        return [start]

    for depth in range(1, MaxDepth + 1):
        visited = {GridToKey(start.grid)}
        result = limited_dfs(start, end, depth, visited)
        if result:
            return result
    return None


# =====================================================
# A* Search (Manhattan heuristic)
# =====================================================
def manhattan_heuristic(start, end):
    """
    Manhattan-style heuristic for A* search.

    Basically pairs up the active cells in start and end states (sorted by position)
    and calculates Manhattan distance between them. Also adds a penalty for any
    difference in the number of active cells.

    This is admissible because Manhattan distance never overestimates - each counter
    needs to be removed at least once, and we're not even accounting for the cost of
    adjacent cells, just the base cost of 1 per move.
    """
    s1 = []
    s2 = []
    for r in range(start.rows):
        for c in range(start.cols):
            if start.grid[r][c] >= 1:
                s1.append((r, c))
            if end.grid[r][c] >= 1:
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
    """A* Search using Manhattan heuristic."""
    if not IsSafe(start) or not IsSafe(end):
        return None
    if StatesEqual(start, end):
        return [start]

    OpenList = [start]
    CameFrom = {}
    g = {GridToKey(start.grid): 0}
    f = {GridToKey(start.grid): manhattan_heuristic(start, end)}
    closed = set()

    while OpenList:
        # Find node with lowest f-score
        current = OpenList[0]
        BestF = f[GridToKey(current.grid)]
        for s in OpenList:
            key = GridToKey(s.grid)
            if f[key] < BestF:
                current = s
                BestF = f[key]

        OpenList.remove(current)
        closed.add(GridToKey(current.grid))

        if StatesEqual(current, end):
            # Reconstruct path
            path = [current]
            key = GridToKey(current.grid)
            while key in CameFrom:
                key = CameFrom[key]
                PrevGrid = [list(r) for r in key]
                PrevState = State(PrevGrid)
                path.insert(0, PrevState)
            return path

        for NextState, pos, cost in current.moves():
            KeyNext = GridToKey(NextState.grid)
            if KeyNext in closed or not IsSafe(NextState):
                continue

            gNew = g[GridToKey(current.grid)] + cost
            if (KeyNext not in g) or (gNew < g[KeyNext]):
                CameFrom[KeyNext] = GridToKey(current.grid)
                g[KeyNext] = gNew
                f[KeyNext] = gNew + manhattan_heuristic(NextState, end)
                InOpen = False
                for s in OpenList:
                    if GridToKey(s.grid) == KeyNext:
                        InOpen = True
                        break
                if not InOpen:
                    OpenList.append(NextState)
    return None


# =====================================================
# Minimum Cost Safe Path (Task 2g - starred)
# =====================================================
def min_safe(start, end):
    """
    Find the minimum-cost safe path using Uniform Cost Search.

    I chose UCS over other algorithms because:
    - It always finds the optimal (lowest cost) path by expanding nodes in order
      of their path cost from the start
    - Doesn't need a heuristic function like A* (which is tricky to get right for
      non-binary states where cells can have different numbers of counters)
    - More straightforward than trying to modify A* to work with variable counter amounts

    Works for both binary and non-binary states.
    """
    if not IsSafe(start) or not IsSafe(end):
        return None

    if StatesEqual(start, end):
        return [start]

    # Priority queue as a list: (cost, state, path)
    Frontier = [(0, start, [start])]

    # Track best cost to reach each state
    BestCost = {GridToKey(start.grid): 0}

    # Closed set
    Closed = set()

    while Frontier:
        # Sort and get lowest cost node
        Frontier.sort(key=lambda x: x[0])
        CurrentCost, Current, Path = Frontier.pop(0)

        CurrentKey = GridToKey(Current.grid)

        if CurrentKey in Closed:
            continue

        Closed.add(CurrentKey)

        # Check if we reached goal
        if StatesEqual(Current, end):
            return Path

        # Explore neighbors
        for NextState, pos, MoveCost in Current.moves():
            NextKey = GridToKey(NextState.grid)

            if not IsSafe(NextState) or NextKey in Closed:
                continue

            NewCost = CurrentCost + MoveCost

            # Update if we found a better path
            if NextKey not in BestCost or NewCost < BestCost[NextKey]:
                BestCost[NextKey] = NewCost
                NewPath = Path + [NextState]
                Frontier.append((NewCost, NextState, NewPath))

    return None


# =====================================================
# Compare algorithms
# =====================================================
def compare(start, end):
    """Print comparison results for all search algorithms."""
    print("\nComparing search algorithms:\n")
    algos = [
        ("BFS", path_BFS),
        ("DFS", path_DFS),
        ("IDDFS", path_IDDFS),
        ("A*", path_astar),
        ("MinSafe", min_safe)
    ]

    for name, func in algos:
        path = func(start, end)
        if path:
            print(f"{name:8} | Success | Path length: {len(path)} | Total cost: {PathCost(path)}")
        else:
            print(f"{name:8} | Failed to find a path.")


# =====================================================
# Tester
# =====================================================
def tester():
    """Test harness for validating search implementations."""
    print("=== a2_path.py tester ===")

    # Test 1: Empty board
    print("\nTest 1: Empty board (start == end)")
    start = State([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    end = State([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    compare(start, end)

    # Test 2: Simple 2x2 block removal
    print("\nTest 2: 2x2 block -> 3 cells")
    start = State([[1, 1, 0], [1, 1, 0], [0, 0, 0]])
    end = State([[1, 1, 0], [1, 0, 0], [0, 0, 0]])
    print(f"Start hingers: {start.numHingers()}, End hingers: {end.numHingers()}")
    compare(start, end)

    # Test 3: Diagonal removal
    print("\nTest 3: 2x2 block -> 2 diagonal cells")
    start = State([[1, 1, 0], [1, 1, 0], [0, 0, 0]])
    end = State([[1, 0, 0], [0, 1, 0], [0, 0, 0]])
    print(f"Start hingers: {start.numHingers()}, End hingers: {end.numHingers()}")
    compare(start, end)

    # Test 4: Larger block
    print("\nTest 4: 2x3 block -> 2x2 block")
    start = State([[1, 1, 1, 0], [1, 1, 1, 0], [0, 0, 0, 0]])
    end = State([[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0]])
    print(f"Start hingers: {start.numHingers()}, End hingers: {end.numHingers()}")
    compare(start, end)

    # Test 5: Clear entire board
    print("\nTest 5: 2x2 block -> empty")
    start = State([[1, 1, 0], [1, 1, 0], [0, 0, 0]])
    end = State([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    print(f"Start hingers: {start.numHingers()}, End hingers: {end.numHingers()}")
    compare(start, end)

    # Test 6: Non-binary state (for min_safe)
    print("\nTest 6: Non-binary state (2 counters -> 1 counter each)")
    start = State([[2, 2, 0], [2, 2, 0], [0, 0, 0]])
    end = State([[1, 1, 0], [1, 1, 0], [0, 0, 0]])
    print(f"Start hingers: {start.numHingers()}, End hingers: {end.numHingers()}")
    compare(start, end)

    # Test 7: Medium complexity
    print("\nTest 7: Medium board with varied counters")
    start = State([
        [1, 1, 1, 0],
        [1, 1, 2, 0],
        [0, 2, 0, 2]
    ])
    end = State([
        [1, 1, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 0, 0]
    ])
    print(f"Start hingers: {start.numHingers()}, End hingers: {end.numHingers()}")
    compare(start, end)


if __name__ == "__main__":
    tester()