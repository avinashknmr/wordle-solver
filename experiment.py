from wordle import Wordle
from solver import WordleSolver

class WordleExperiment:
    def __init__(self, word=None):
        self.wordle = Wordle(word)
        self.solver = WordleSolver()
    
    def solve(self):
        return self.solver.solve(self.wordle, False)