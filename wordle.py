from utils import dictionary, wordle_words, LETTER_COUNT, ATTEMPT_LIMIT, GameResult, CharResult
import random

class Wordle:
    def __init__(self):
        self.attempt = 0
        self.dictionary = dictionary()
        self.wordle_words = wordle_words()

    def reset(self):
        self.attempt = 0
        self.word = self._get_new_word()
    
    def _get_new_word(self):
        return random.choice(self.wordle_words)

    def set_word(self, word):
        self.word = word

    def check_answer(self, guess):
        if self.attempt < ATTEMPT_LIMIT:
            if len(guess)!=LETTER_COUNT:
                return GameResult.INVALID_TRY, None
            if guess not in self.dictionary:
                return GameResult.INVALID_WORD, None
            self.attempt += 1
            tiles = []
            result = GameResult.FAILED_ATTEMPT
            for i, c in enumerate(guess):
                if c == self.word[i]:
                    tiles.append(CharResult.GREEN)
                elif c in self.word:
                    tiles.append(CharResult.YELLOW)
                else:
                    tiles.append(CharResult.BLACK)
            if all([t=='g' for t in tiles]):
                result = GameResult.WON
            elif self.attempt == ATTEMPT_LIMIT:
                result = GameResult.LOST
            return result, ''.join(tiles)
        return GameResult.LOST, None