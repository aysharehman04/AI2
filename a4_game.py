# a4_game.py
"""
Group ID: B1
Student ID: 
100464246
100428936


"""
"""
State class for the Hinger game
"""

from a1_state import State
from a3_agent import Agent


def play(state, agentA, agentB):
    """
    Play a complete game between two agents or human players.

    agentA/agentB can be Agent objects or None (for human player).
    Returns the name of the winner, or None for a draw.
    """
    CurrentState = state
    Players = [agentA, agentB]
    PlayerNames = [
        agentA.name if agentA else "Human A",
        agentB.name if agentB else "Human B"
    ]
    Turn = 0
    MoveCount = 0

    print("=== Starting Hinger Game ===")
    print(f"Player 1: {PlayerNames[0]}")
    print(f"Player 2: {PlayerNames[1]}")
    print("\nInitial board:")
    print(CurrentState)
    print()

    while True:
        CurrentPlayer = Players[Turn]
        CurrentName = PlayerNames[Turn]

        print(f"\n--- Turn {MoveCount + 1}: {CurrentName}'s move ---")
        print("Current board:")
        print(CurrentState)
        print()

        IsEmpty = True
        for r in range(CurrentState.rows):
            for c in range(CurrentState.cols):
                if CurrentState.grid[r][c] > 0:
                    IsEmpty = False
                    break
            if not IsEmpty:
                break

        if IsEmpty:
            print("All counters removed - DRAW!")
            return None

        if CurrentPlayer is None:
            Move = GetHumanMove(CurrentState)
        else:
            Move = GetAgentMove(CurrentPlayer, CurrentState)
            print(f"DEBUG: Agent returned move {Move}")

        if Move is None:
            print(f"Invalid move by {CurrentName}!")
            OpponentName = PlayerNames[1 - Turn]
            print(f"{OpponentName} wins!")
            return OpponentName

        r, c = Move
        if not IsValidMove(CurrentState, r, c):
            print(f"Illegal move by {CurrentName} at {Move}!")
            OpponentName = PlayerNames[1 - Turn]
            print(f"{OpponentName} wins!")
            return OpponentName

        WasHinger = IsHinger(CurrentState, r, c)

        NewGrid = [row[:] for row in CurrentState.grid]
        NewGrid[r][c] -= 1
        CurrentState = State(NewGrid)

        print(f"{CurrentName} moves at {Move}")
        MoveCount += 1

        if WasHinger:
            print("\nFinal board:")
            print(CurrentState)
            print(f"\n{CurrentName} hit a HINGER and WINS!")
            return CurrentName

        Turn = 1 - Turn


def GetHumanMove(state):
    try:
        print("Enter your move (row col): ", end="")
        Inp = input().strip()
        Parts = Inp.split()
        if len(Parts) != 2:
            return None
        r = int(Parts[0])
        c = int(Parts[1])
        return (r, c)
    except:
        return None


def GetAgentMove(agent, state):
    """Get move from agent using its default strategy."""
    try:
        Mode = agent.modes[0] if agent.modes else 'minimax'
        Score, Move = agent.move(state, Mode)
        print(f"Agent chose move {Move} with score {Score}")
        return Move
    
    except:
        return None


def IsValidMove(state, r, c):
    if r < 0 or r >= state.rows or c < 0 or c >= state.cols:
        return False
    if state.grid[r][c] <= 0:
        return False
    return True


def IsHinger(state, r, c):
    if state.grid[r][c] != 1:
        return False

    OriginalRegions = state.numRegions()

    TestGrid = [row[:] for row in state.grid]
    TestGrid[r][c] = 0
    TestState = State(TestGrid)
    NewRegions = TestState.numRegions()

    return NewRegions > OriginalRegions


def tester():
    print("--- a4_game.py tester ---\n")

    # Test 1: agent vs agent
    print("Test 1: Agent vs Agent")
    TestGrid = [
        [1, 1, 0],
        [1, 1, 0],
        [0, 0, 0]
    ]
    TestState = State(TestGrid)
    AgentA = Agent((3, 3), "Alpha")
    AgentB = Agent((3, 3), "Beta")

    Winner = play(TestState, AgentA, AgentB)
    print(f"\nResult: {Winner if Winner else 'Draw'}\n")

    # Test 2: smaller game
    print("\n" + "-" * 50)
    print("Test 2: Smaller board")
    TestGrid2 = [
        [1, 1],
        [1, 0]
    ]
    TestState2 = State(TestGrid2)
    AgentC = Agent((2, 2), "Charlie")
    AgentD = Agent((2, 2), "Delta")

    Winner2 = play(TestState2, AgentC, AgentD)
    print(f"\nResult: {Winner2 if Winner2 else 'Draw'}\n")

    # Test 3: example with potential hinger
    print("\n" + "-" * 50)
    print("Test 3: Board with hinger")
    TestGrid3 = [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1]
    ]
    TestState3 = State(TestGrid3)
    print(f"Initial hingers: {TestState3.numHingers()}")
    AgentE = Agent((3, 3), "Echo")
    AgentF = Agent((3, 3), "Foxtrot")

    Winner3 = play(TestState3, AgentE, AgentF)
    print(f"\nResult: {Winner3 if Winner3 else 'Draw'}\n")

    Winner = play(TestState, None, AgentB)  # Human vs agent running off of Test 1
    Winner = play(TestState, None, None)  # Human vs human running off of Test 1

    Winner = play(TestState3, None, AgentE)  # Human vs Agent
    Winner = play(TestState3, None, None)  # Human vs Human


if __name__ == "__main__":
    tester()