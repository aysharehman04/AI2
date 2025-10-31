"""
Agent class for the Hinger Game


"""
from a1_state import State
import timeit

class Agent:
    def __init__(self, size, name='B1'):
        self.size = size
        self.name = name
        self.modes = ['minimax', 'alphabeta']

    def __str__(self):
        return f"Agent name: {self.name}, Board size: {self.size} Modes: {self.modes}"
    

    def win(self, state):
        return state.numHingers() > 0
    
    
    def is_terminal(self, state):
    
        # need section for checking if there is a win
        if self.win(state):
        #    print("this state is a winner state ")          Sorry just had to comment this out as it was being
            return True                                     #called everytime minimax evaluated causing massive repeated outputs
                                                            #-Luca
        for rows in state.grid:
            for cell in rows:
                if cell > 0 : 
                     # found a move
                    # print("found a possible move ")
                    return False
      #  print("no possible moves found")                   Same as above^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        return True  # no moves found
    
    def evaluate(self,state):
        total_move_cost = sum(state.move_cost(r, c)
                          for r in range(state.rows)
                          for c in range(state.cols)
                          if state.grid[r][c] > 0)
    
         # Fewer hingers is better
        hinger_score = -state.numHingers()
        
        # More regions is better
        region_score = state.numRegions()
        
        # Weighted sum
        score = total_move_cost + 2 * region_score + 3 * hinger_score
        return score
    
    def find_diff(self, old_state, new_state):
        """Return (i, j) of the cell that changed between two states."""
        for i in range(len(old_state.grid)):
            for j in range(len(old_state.grid[0])):
                if old_state.grid[i][j] != new_state.grid[i][j]:
                    return (i, j)
        return None
    
    

    def move(self, state, mode):
        print(f"Agent {self.name} using {mode.upper()} strategy...")
        if mode == "minimax":
            return self.minimax_move(state)
        if mode == "alphabeta":
            return self.alphabeta_move(state)
        else:
            raise ValueError(f"Unknown mode: {mode}") 
       
          
        
    def minimax_move(self, state, depth = 3, max_player = True):

        #base case:
        if depth == 0 or self.is_terminal(state):
            score =  self.evaluate(state)
            # print(f"Depth {depth}, Player {'MAX' if max_player else 'MIN'}, Evaluated score: {score}")
            return score, None
        
        if max_player:
            best_score = float('-inf')
            best_move = None
            for new_state, move, cost in state.moves():
                score, _ = self.minimax_move(new_state, depth-1, False)
                if score > best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move
        else:
            best_score = float('inf')
            best_move = None
            for new_state, move, cost in state.moves():
                score, _ = self.minimax_move(new_state, depth-1, True)
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


    #best_move = agent.minimax_move(sa)
    #print(best_move)
    # sa_grid1 = [
    #         [0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0]
    # ]
    # sa1 = State(sa_grid1)
    # print(agent.is_terminal(sa1))
   
    # sa_grid3 = [
    #         [0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0]
    # ]
    # sa3 = State(sa_grid3)
    # print(agent.is_terminal(sa3))


if __name__ == "__main__":
     tester()


 

    
    