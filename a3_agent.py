"""
Agent class for the Hinger Game


"""
from a1_state import State
class Agent:
    def __init__(self, size, name="B1"):
        self.size = size
        self.name = name

    def __str__(self):
        out = f" Agent namw: {self.name}"
        out += f"playing {self.size} hinge game"
        return out
    
    def move(self, state, mode):
        pass

    
    