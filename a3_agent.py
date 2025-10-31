"""
Group ID: B1
Student ID: 
100464246
100428936
100435561
"""
"""
Agent class for the Hinger game
"""

from a1_state import State
import timeit

class Agent:
    """
    a. Initialiser, which receives two parameters: size and name. The first
    parameter size represents the board size as a tuple (m,n), where m is the
    number of rows and n is the number of columns. The second parameter
    name is an optional string representing the agent’s name, with your group
    name as the default value. The initialiser should set up the agent accordingly.
    """ 
    def __init__(self, size, name='B1'):
        self.size = size
        self.name = name
        self.modes = ['minimax', 'alphabeta']

    """
    b. A sensible __str__ method.
    """
    def __str__(self):
        return f"Agent name: {self.name}, Board size: {self.size} Modes: {self.modes}"
    
    """
    c. Method move(state, mode) that receives a State object representing the
    current game board and a playing strategy, and returns a legitimate move for your agent (e.g. a cell position (𝑖, 𝑗) to act on). 
    If no move is possible (e.g.there are no active cells), return None. Use the best strategy you have
    implemented as the default value for the mode parameter.
    """
    def move(self, state, mode):
        print(f"Agent {self.name} using {mode.upper()} strategy...")
        if mode == "minimax":
            return self.minimax_move(state)
        if mode == "alphabeta":
            return self.alphabeta_move(state)
        else:
            raise ValueError(f"Unknown mode: {mode}") 

    """
    d. Additional supporting methods as needed to facilitate decision-making and
    strategy implementation for playing a binary Hinger game (that is, the game
    starts with a binary state). Your modes list should contain (i) an element
    named ‘minimax’, for which your agent plays using the minimax strategy, and
    (ii) an element named ‘alphabeta’, for which the agent plays using the alpha-
    beta pruning strategy.
    """    

    def win(self, state):
       return all(cell == 0 for row in state.grid for cell in row)
    
    
    def is_terminal(self, state):
        if self.win(state):  
            return True                                     
        for rows in state.grid:
            for cell in rows:
                if cell > 0 : 
                    return False
        return True
    
    def evaluate(self,state):
        if self.win(state):
            return float('inf')

        hingers = state.numHingers()
        regions = state.numRegions()
        total_counters = sum(sum(row) for row in state.grid)
        moves_available = sum(
            1 for r in range(state.rows)
            for c in range(state.cols)
            if state.grid[r][c] > 0
        )

        # New: position-based score
        center_r, center_c = state.rows // 2, state.cols // 2
        position_score = 0
        for r in range(state.rows):
            for c in range(state.cols):
                if state.grid[r][c] > 0:
                    # closer to center gets a bonus
                    dist = abs(center_r - r) + abs(center_c - c)
                    position_score += (2 - dist)

        score = (
            hingers * 20
            + regions * 5
            + moves_available * 2
            - total_counters * 1.5
            + position_score * 1.2
        )

        return score
       
    def minimax_move(self, state, depth = 3, max_player = True, root = True):
        #base case:
        if depth == 0 or self.is_terminal(state):
            # print(f"Depth {depth}, Player {'MAX' if max_player else 'MIN'}, Evaluated score: {score}")
        
            return self.evaluate(state), None
        
        if max_player:
            best_score = float('-inf')
            best_move = None
            for new_state, move, cost in state.moves():
                score, _ = self.minimax_move(new_state, depth-1, False, root = False)
                if root:
                    print(f"Move {move} -> score {score}")
                if score > best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move
        else:
            best_score = float('inf')
            best_move = None
            for new_state, move, cost in state.moves():
                score, _ = self.minimax_move(new_state, depth-1, True, root = False)
                if score < best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move

    
    def alphabeta_move(self, state,alpha=float("-inf"), beta=float("inf"), depth = 3, max_player= True):
        #base case:
        if depth == 0 or self.is_terminal(state):
            score =  self.evaluate(state)
            # print(f"Depth {depth}, Player {'MAX' if max_player else 'MIN'}, Evaluated score: {score}")
            return score, None
        
        if max_player:
            max_score = float('-inf')
            best_move = None
            for new_state, move, cost in state.moves():
                score, _ = self.alphabeta_move(new_state, alpha, beta, depth-1, False)
                if score > max_score:
                    max_score = score
                    best_move = move

                alpha = max(alpha, max_score)
                if alpha >= beta:
                    break   # β cutoff → prune

            return max_score, best_move
        else:
            min_score = float('inf')
            best_move = None
            for new_state, move, cost in state.moves():
                score, _ = self.alphabeta_move(new_state,alpha, beta, depth-1, True)
                if score < min_score:
                   min_score = score
                   best_move = move
                beta = min(beta, min_score)
                if beta <= alpha:
                    break   # α cutoff → prune
            return min_score, best_move

"""
Tester 
"""
def tester():
    print("Agent tester:")

    agent = Agent((5,4))
    print(agent)
    sa_grid2 = [
            [1, 1, 0, 0, 2],
            [1, 1, 0, 0, 0],
            [0, 0, 1, 1, 1],
            [0, 0, 0, 1, 1]
    ]
    state = State(sa_grid2)
    print("Is terminal?",agent.is_terminal(state))
    print("\n")


    print("Testing Minimax:")
    def run_minimax():
        score, move = agent.minimax_move(state)
        # print(score, move)
        print("\n")

    avg_time = timeit.timeit(run_minimax, number=10) / 10
    print(f"Average Minimax time over 10 runs: {avg_time:.6f} seconds")

    print("Testing Alphabeta:")
    def run_alphabeta():
        score, move = agent.alphabeta_move(state)
        # print(score, move)
        print("\n")

    avg_time = timeit.timeit(run_alphabeta, number=10) / 10
    print(f"Average alphabeta time over 10 runs: {avg_time:.6f} seconds")

    sa_grid3 = [
            [1, 1, 0, 0, 1],
            [1, 1, 0, 0, 0],
            [0, 0, 1, 1, 1],
            [0, 0, 0, 1, 1]
    ]
    state2 = State(sa_grid3)
    print("Is terminal?",agent.is_terminal(state2))
    print("Is winning pos?",agent.win(state2))

if __name__ == "__main__":
     tester()


 

    
    