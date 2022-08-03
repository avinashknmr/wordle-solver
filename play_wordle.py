from wordle import Wordle
from solver import WordleSolver
from utils import LETTER_COUNT, ATTEMPT_LIMIT, GuessResult, GameResult
import re

class Game(Wordle):
    def __init__(self):
        super().__init__()
    
    def _parse_answer(self, guess: str, game_verdict: str):
        if len(guess)!=LETTER_COUNT:
            return GameResult.INVALID_TRY, None
        if guess not in self.dictionary:
            return GameResult.INVALID_WORD, None
        elif not re.match("[gyb]+", game_verdict.lower()):
            print("Give a valid string containing only 'GYB' E.g. 'GGYBY")
            return None
        tiles = []
        result = GameResult.FAILED_ATTEMPT
        for c in game_verdict:
            if c == 'g':
                tiles.append(GuessResult.GREEN)
            elif c == 'y':
                tiles.append(GuessResult.YELLOW)
            elif c == 'b':
                tiles.append(GuessResult.BLACK)
        if all([t=='g' for t in tiles]):
            result = GameResult.WON
        elif self.attempt == ATTEMPT_LIMIT:
            result = GameResult.LOST
        return result, ''.join(tiles)

    def check_answer(self, guess):
        while self.attempt < ATTEMPT_LIMIT:
            print(f'Try: {guess}')
            game_verdict = input("What did the game say: ")
            result = self._parse_answer(guess, game_verdict)
            if result is None:
                continue
            else:
                self.attempt += 1
                return result
        return GameResult.LOST, None

    def play(self, solver: WordleSolver):
        solver.reset()
        solver.solve(self)

if __name__ == '__main__':
    game = Game()
    game.play(WordleSolver())