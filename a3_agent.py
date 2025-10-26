"""
Agent class for the Hinger Game


"""
from a1_state import State

class Agent:
    def __init__(self, size, name='B1'):
        self.size = size
        self.name = name
        self.modes = ['minimax', 'alphabeta']

    def __str__(self):
        return f"Agent name: {self.name}, Board size: {self.size} 'Modes: {self.modes}"
    

    def win(self, state):
        return state.numHingers == 1
    

    
        
    def is_terminal(self, state):
        #need section for checking if there is a win
        if self.win(state):
            return True
        
        for row in state.grid:
            for cell in row:
                if cell > 0:  # found a move
                    return False
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
    
    

    def move(self, state, mode):
        if mode == "minimax":
            return self.minimax_move(state)
        if mode == "alphabeta":
            return self.alphabeta_move(state)
        else:
            raise ValueError(f"Unknown mode: {mode}") 
          
        
    def minimax_move(self, state, depth = 3, max_player = True):

        #base case:
        if depth == 0 or state.is_terminal():
            return self.evaluate(state), None
        
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

    
    def alphabeta_move(self, state,alpha=float("-inf"), beta=float("-inf"), depth = 3, max_player= True):
        #base case:
        if depth == 0 or state.is_terminal():
            return self.evaluate(state), None
        
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
    print("Agent state tester:")

    # sa_grid = [
    #         [2, 1, 0, 0, 0],
    #         [0, 1, 0, 1, 0],
    #         [1, 0, 2, 0, 1],
    #         [0, 0, 0, 1, 0]
    # ]
    # sa = State(sa_grid)

    # print("\nState A:")
    # print(sa)
    # print("\nPossible moves from State A:")
    # for new_state, pos, cost in sa.moves():
    #     print(f"Move at {pos} (cost {cost}):")
    #     print(new_state)
    #     print("----")
    
    agent = Agent((5,4))
    print(agent)

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
    sa_grid2 = [
            [1, 1, 0, 0, 1],
            [1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 1, 1]
    ]
    sa2 = State(sa_grid2)
    print(agent.is_terminal(sa2))


if __name__ == "__main__":
     tester()


 

    
    