# a1_state.py
"""
Group ID: B1
Student IDs:
100464246
100428936




"""
"""
State class for the Hinger game

"""
from copy import deepcopy
class State:
    def __init__(self, grid):
        """
        a. A proper initialiser, which receives a 2D list grid as a parameter, representing
        the number of counters in each cell.
        """
        assert all(len(row) == len(grid[0]) for row in grid)
        self.grid = [row[:] for row in grid]
        self.rows = len(grid)
        self.cols = len(grid[0])
    
    def __str__(self):
        """
        b. A sensible __str__ method, which returns a readable string representation of
        the state (e.g., a matrix similar to those in Figure 1, without borders).
        """
        return '\n'.join(' '.join(str(cell) for cell in row) for row in self.grid)
    
    def moves(self):
        """
        c. A generator method named moves() that yields all possible states reachable
        in one move (i.e., removing one counter from any active cell).
        Each yeilded value is a truple (new_state, move_position, move_cost)
        """
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] > 0:
                    new_state = self.clone()
                    new_state.grid[r][c] -= 1
                    yield (new_state, (r,c), self.move_cost(r, c))
 
       
    def numRegions(self):
        """
        d. A method numRegions() that calculates and returns the number of active
        regions on the board.
        """
        visited = [[False]*self.cols for _ in range(self.rows)]
        regions = 0

        def bfs(sr, sc):
            queue = [(sr, sc)]
            visited[sr][sc] = True
            while queue:
                r, c = queue.pop(0)
                for dr, dc in self.directions():
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        if self.grid[nr][nc] > 0 and not visited[nr][nc]:
                            visited[nr][nc] = True
                            queue.append((nr,nc))

        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] > 0 and not visited[r][c]:
                    bfs(r,c)
                    regions += 1
        return regions
    
    def numHingers(self):
        """
        e. A method numHingers() that returns the number of hinger cells in the current
        state.
        A hinger is a cell with 1 counter that, when removed, increases the number of regions.
        """
        original_regions = self.numRegions()
        hinger_count = 0

        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == 1:
                    self.grid[r][c] = 0
                    new_regions = self.numRegions()
                    self.grid[r][c] = 1

                    if new_regions > original_regions:
                        hinger_count += 1

        return hinger_count
    
    def directions(self):
        """
        f. Any additional utility methods that support gameplay logic or improve code
        clarity.
        Returns all directions a player can move.
        """
        return [
            (-1,-1), #diagonal up-left
            (-1,0),  # above 
            (-1,1),  # diagonal up-right
            (0,-1),  # left
            (0,1),   # right
            (1,-1),  # diagonal down-left
            (1,0),   # down
            (1,1)    # diagonal down-right
        ]
    

    
    def move_cost(self, r, c):
        """
        f. Any additional utility methods that support gameplay logic or improve code
        clarity.
        Returns the cost of a move at a cell (r, c)
        Cost is 1 + the number of active adjacent cells.
        Additional utility to support game play.
        """
        cost = 1
        for dr, dc in self.directions():
            nr, nc = r+dr, c+dc 
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.grid[nr][nc] > 0:
                    cost += 1
        return cost
    
    def clone(self):
        """
        f. Any additional utility methods that support gameplay logic or improve code
        clarity.
        Returns a deepcopy of the state.
        Used from Taoyangs code from lab1 part 2
        https://docs.python.org/3.12/library/copy.html
        """
        return State([row[:] for row in self.grid])
        # """Return a deep copy of the state."""
        # return deepcopy(self)
        
    
def tester():
        """
        Within this file, define a test function named tester() to validate your
        implementation. This function should execute automatically when the script
        a1_state.py is run directly, but not when imported as a module. Inside this
        function, implement the following tasks:
        i. Create a State instance named sa representing State A from Figure 1,
        and print its string representation.
        ii. Implement additional testing cases to verify your implementation. 
        """
        print("Hinger state tester:")

        sa_grid = [
            [1, 2, 0, 1, 0],
            [0, 0, 1, 2, 0],
            [1, 0, 2, 0, 0],
            [0, 1, 0, 1, 0]
        ]
        sa = State(sa_grid)

        print("\nState A:")
        print(sa)

        print("\nNumber of active regions:", sa.numRegions())
        print("Number of hinger cells:", sa.numHingers())

        print("\nPossible moves from State A:")
        for new_state, pos, cost in sa.moves():
            print(f"Move at {pos} (cost {cost}):")
            print(new_state)
            print("----")

        test_grid = [
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1]
        ]
        print(State(test_grid).numHingers())
        
    
if __name__ == "__main__":
     tester()





    

                       



    
