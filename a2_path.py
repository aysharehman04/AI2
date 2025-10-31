# a2_path.py
"""
Group ID: B1
Student ID: 
100464246
100428936
100435561
"""
"""
Contains a set of functions for determining and retrieving safe paths
between states in the Hinger game, along with a test harness to validate and
compare implementations.

This module implements the following algorithms:
  - path_BFS
  - path_DFS
  - path_IDDFS
  - path_astar
  - min_safe
"""

from a1_state import State
"""
Helper functions
"""
def GridToKey(grid):
    """
    Converts a 2D grid into a tuple of tuples so it can be hashed/compared.
    Useful for storing visited states in sets/dictionaries.
    """
    return tuple(tuple(row) for row in grid)


def StatesEqual(s1, s2):
    """Returns True if two states have identical grids, if so that goal state
    has been reached.
    """
    return s1.grid == s2.grid


def IsSafe(state):
    """Returns True if a state is safe (state has no hingers)."""
    return state.numHingers() == 0


def ApplyMoves(start, moves):
    """Apply a sequence of moves to get to the final state."""
    Current = start
    for move in moves:
        r, c = move
        NewGrid = [row[:] for row in Current.grid]
        NewGrid[r][c] -= 1
        Current = State(NewGrid)
    return Current


def MoveCost(state, move):
    """
    Get the cost of a move at a specific cell (r, c).
    Used in PathCost and min_safe for calculating total path costs.
    """
    r, c = move
    return state.move_cost(r, c)


def PathCost(start, moves):
    """Finds out the total cost of a path."""
    Total = 0
    Current = start
    for move in moves:
        Total += MoveCost(Current, move)
        r, c = move
        NewGrid = [row[:] for row in Current.grid]
        NewGrid[r][c] -= 1
        Current = State(NewGrid)
    return Total

"""
a. A function path_BFS(start,end) that receives two binary states, start and end,
and returns a safe path (as a list of moves) if such a path exists, or None
otherwise, using the Breadth-First Search (BFS) algorithm.

Justification for BFS:
Uses a queue to explore all possible paths level by level.
BFS guarantees finding a path if one exists.
BFS finds the shortest path.
Simple to implement and understand.
"""
def path_BFS(start, end):
    if not IsSafe(start) or not IsSafe(end):
        return None
    if StatesEqual(start, end):
        return []

    Frontier = [(start, [])]
    Visited = {GridToKey(start.grid)}

    while Frontier:
        Current, Moves = Frontier.pop(0)
        for NextState, pos, cost in Current.moves():
            Key = GridToKey(NextState.grid)
            if Key in Visited:
                continue
            if not IsSafe(NextState):
                continue
            Visited.add(Key)
            NewMoves = Moves + [pos]
            if StatesEqual(NextState, end):
                return NewMoves
            Frontier.append((NextState, NewMoves))
    return None

"""
b. A function path_DFS(start, end) which receives two binary states, start and
end, and returns a safe path (as a list of moves) if such a path exists, or None
otherwise, using the Depth-First Search (DFS) algorithm.

Justification for DFS:
Uses a stack to explore as deep as possible along each path before backtracking.
DFS can be more memory efficient than BFS for deep search spaces.
DFS can find a path quickly in some scenarios, though not guaranteed to be shortest.
"""
def path_DFS(start, end, limit=10000):
    if not IsSafe(start) or not IsSafe(end):
        return None
    if StatesEqual(start, end):
        return []

    Stack = [(start, [])]
    Visited = {GridToKey(start.grid)}

    Steps = 0
    while Stack:
        Current, Moves = Stack.pop()
        Steps += 1
        if Steps > limit:
            return None
        for NextState, pos, cost in Current.moves():
            Key = GridToKey(NextState.grid)
            if Key in Visited:
                continue
            if not IsSafe(NextState):
                continue
            Visited.add(Key)
            NewMoves = Moves + [pos]
            if StatesEqual(NextState, end):
                return NewMoves
            Stack.append((NextState, NewMoves))
    return None


def limited_dfs(Current, end, depth, Visited, Moves):
    """Building block for IDDFS, allows IDDFS to explore shallower depths first."""
    if StatesEqual(Current, end):
        return Moves
    if depth == 0:
        return None
    for NextState, pos, cost in Current.moves():
        Key = GridToKey(NextState.grid)
        if Key in Visited or not IsSafe(NextState):
            continue
        Visited.add(Key)
        Result = limited_dfs(NextState, end, depth - 1, Visited, Moves + [pos])
        Visited.remove(Key)
        if Result is not None:
            return Result
    return None

"""
c. A function path_
IDDFS(start, end) which receives two binary states, start and
end, and returns a safe path (as a list of moves) if such a path exists, or None
otherwise, using the Iterative Deepening Depth-First Search (IDDFS).

Justification for IDDFS:
Combines benefits of BFS (completeness) and DFS (space efficiency).
Explores shallower depths first, which can find solutions quickly in some cases.
"""
def path_IDDFS(start, end, MaxDepth=50):
    if not IsSafe(start) or not IsSafe(end):
        return None
    if StatesEqual(start, end):
        return []

    for depth in range(1, MaxDepth + 1):
        Visited = {GridToKey(start.grid)}
        Result = limited_dfs(start, end, depth, Visited, [])
        if Result is not None:
            return Result
    return None


"""
Manhattan heuristic for A* search

Justification for Manhattan Heuristic:
Provides a reasonable estimate of distance.
"""
def manhattan_heuristic(start, end):
    S1 = []
    S2 = []
    for r in range(start.rows):
        for c in range(start.cols):
            if start.grid[r][c] >= 1:
                S1.append((r, c))
            if end.grid[r][c] >= 1:
                S2.append((r, c))

    S1.sort()
    S2.sort()

    Total = 0
    Length = min(len(S1), len(S2))
    for i in range(Length):
        r1, c1 = S1[i]
        r2, c2 = S2[i]
        Total += abs(r1 - r2) + abs(c1 - c2)

    Total += abs(len(S1) - len(S2))
    return Total

"""
d. A function path_astar(start,end) which receives two binary states, start and
end, and returns a safe path if one exists, or None otherwise, using the A*
search algorithm.

Justification for A* Search:
A* is efficient and finds optimal paths using heuristics.
Explores paths with the lowest estimated total cost first.
Faster on larger boards.
Combines benefits of uniform cost search (optimality) with heuristics (speed).
"""
def path_astar(start, end):
    if not IsSafe(start) or not IsSafe(end):
        return None
    if StatesEqual(start, end):
        return []

    OpenList = [start]
    CameFrom = {}
    MoveTo = {}
    g = {GridToKey(start.grid): 0}
    f = {GridToKey(start.grid): manhattan_heuristic(start, end)}
    Closed = set()

    while OpenList:
        Current = OpenList[0]
        BestF = f[GridToKey(Current.grid)]
        for s in OpenList:
            Key = GridToKey(s.grid)
            if f[Key] < BestF:
                Current = s
                BestF = f[Key]

        OpenList.remove(Current)
        Closed.add(GridToKey(Current.grid))

        if StatesEqual(Current, end):
            Moves = []
            Key = GridToKey(Current.grid)
            while Key in CameFrom:
                Moves.insert(0, MoveTo[Key])
                Key = CameFrom[Key]
            return Moves

        for NextState, pos, cost in Current.moves():
            KeyNext = GridToKey(NextState.grid)
            if KeyNext in Closed or not IsSafe(NextState):
                continue

            gNew = g[GridToKey(Current.grid)] + cost
            if (KeyNext not in g) or (gNew < g[KeyNext]):
                CameFrom[KeyNext] = GridToKey(Current.grid)
                MoveTo[KeyNext] = pos
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

"""
g. [*] A function min_safe(start,end) which receives two states start and end
(which are not necessary binary), and returns a safe path with the minimal
cost (i.e., the safe path with the lowest total sum of move costs) if such a
path exists. Otherwise, it should return None.

Justification for Uniform Cost Search:
Expands lowest cost path first.
Doesn't need a heuristic like A* (hard to make one for non-binary states).
Works for any number of counters per cell.
"""

def min_safe(start, end):
    if not IsSafe(start) or not IsSafe(end):
        return None

    if StatesEqual(start, end):
        return []

    Frontier = [(0, start, [])]
    BestCost = {GridToKey(start.grid): 0}
    Closed = set()

    while Frontier:
        Frontier.sort(key=lambda x: x[0])
        CurrentCost, Current, Moves = Frontier.pop(0)

        CurrentKey = GridToKey(Current.grid)

        if CurrentKey in Closed:
            continue

        Closed.add(CurrentKey)

        if StatesEqual(Current, end):
            return Moves

        for NextState, pos, MoveCost in Current.moves():
            NextKey = GridToKey(NextState.grid)

            if not IsSafe(NextState) or NextKey in Closed:
                continue

            NewCost = CurrentCost + MoveCost

            if NextKey not in BestCost or NewCost < BestCost[NextKey]:
                BestCost[NextKey] = NewCost
                NewMoves = Moves + [pos]
                Frontier.append((NewCost, NextState, NewMoves))

    return None

"""
f. A test function named tester() to test the functions you implemented.
Function compare() to evaluate and compare the performance of the
four search algorithms (BFS,DFS, IDDFS, and A*) in finding a safe path
between two game states in Hinger.
"""
def compare(start, end):
    print("\nComparing search algorithms:\n")
    Algos = [
        ("BFS", path_BFS),
        ("DFS", path_DFS),
        ("IDDFS", path_IDDFS),
        ("A*", path_astar),
        ("MinSafe", min_safe)
    ]

    for name, func in Algos:
        Moves = func(start, end)
        if Moves is not None:
            Cost = PathCost(start, Moves) if Moves else 0
            print(f"{name:8} | Success | Path length: {len(Moves)} | Total cost: {Cost}")
        else:
            print(f"{name:8} | Failed to find a path.")


"""
Tester 
"""
def tester():
    print("--- a2_path.py tester ---")

    # Test 1: small case
    print("\nTest 1: Empty board (start == end)")
    start = State([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    end = State([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    compare(start, end)

    # Test 2: simple removal
    print("\nTest 2: 2x2 block -> 3 cells")
    start = State([[1, 1, 0], [1, 1, 0], [0, 0, 0]])
    end = State([[1, 1, 0], [1, 0, 0], [0, 0, 0]])
    print(f"Start hingers: {start.numHingers()}, End hingers: {end.numHingers()}")
    compare(start, end)

    # Test 3: diagonal
    print("\nTest 3: 2x2 block -> 2 diagonal cells")
    start = State([[1, 1, 0], [1, 1, 0], [0, 0, 0]])
    end = State([[1, 0, 0], [0, 1, 0], [0, 0, 0]])
    print(f"Start hingers: {start.numHingers()}, End hingers: {end.numHingers()}")
    compare(start, end)

    # Test 4: bigger block
    print("\nTest 4: 2x3 block -> 2x2 block")
    start = State([[1, 1, 1, 0], [1, 1, 1, 0], [0, 0, 0, 0]])
    end = State([[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0]])
    print(f"Start hingers: {start.numHingers()}, End hingers: {end.numHingers()}")
    compare(start, end)

    # Test 5: clear board
    print("\nTest 5: 2x2 block -> empty")
    start = State([[1, 1, 0], [1, 1, 0], [0, 0, 0]])
    end = State([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    print(f"Start hingers: {start.numHingers()}, End hingers: {end.numHingers()}")
    compare(start, end)

    # Test 6: non-binary (multiple counters)
    print("\nTest 6: Non-binary state")
    start = State([[2, 2, 0], [2, 2, 0], [0, 0, 0]])
    end = State([[1, 1, 0], [1, 1, 0], [0, 0, 0]])
    print(f"Start hingers: {start.numHingers()}, End hingers: {end.numHingers()}")
    compare(start, end)

    # Test 7: varied counters
    print("\nTest 7: Medium board")
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

    # Test 8: Showing and comparing steps for each algorithm
    print("\n--- Search Algorithm Comparisons ---")
    start = State([[1, 1, 0], [1, 1, 0], [0, 0, 0], [1,2, 1]])
    end = State([[1, 1, 0], [1, 0, 0], [0, 0, 0], [1,0, 0]])

    searchAlgorithms = {
        "BFS": path_BFS,
        "DFS": path_DFS,
        "IDDFS": path_IDDFS,
        "A*": path_astar,
        "MinSafe": min_safe,
    }

    for name, func in searchAlgorithms.items():
        print(f"\n--- {name} Testing Example showing moves ---")
        Moves = func(start, end)

        if Moves:
            print(f"Moves: {Moves}")
            print("Start state:")
            print(start)
            Current = start
            for i, move in enumerate(Moves):
                r, c = move
                print(f"\nMove {i + 1} at {move}:")
                NewGrid = [row[:] for row in Current.grid]
                NewGrid[r][c] -= 1
                Current = State(NewGrid)
                print(Current)
        else:
            print(f"No valid moves found with {name}.")


if __name__ == "__main__":
    tester()