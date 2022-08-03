from utils import dictionary, wordle_words, LETTER_COUNT, ATTEMPT_LIMIT, GameResult, GuessResult
import string
from collections import Counter
import random

class WordleSolver:
    def __init__(self):
        self._all_possible_words = set(dictionary())
        self._possible_words = set(dictionary())
        self._green_chars = set()
        self._invalid_chars = set()
        self._yellow_chars = set()
        self._untried_chars = set(i for i in string.ascii_lowercase)
        self.attempts = 0
        self.tries = []
    
    def reset(self):
        self._possible_words = set(dictionary())
        self._green_chars.clear()
        self._invalid_chars.clear()
        self._yellow_chars.clear()
        self._untried_chars = set(i for i in string.ascii_lowercase)
        self.attempts = 0
        self.tries.clear()
    
    def __get_probability_scores(self, words):
        untried_letter_probability = Counter()
        freq_map = Counter()
        for w in words:
            for c in w:
                if c in self._untried_chars:
                    untried_letter_probability[c] += 1
                freq_map[c] += 1
        return untried_letter_probability, freq_map

    def __contains_invalid_chars(self, word):
        for letter in word:
            if letter in self._invalid_chars:
                return True
        return False

    def __contains_yellow_chars(self, word):
        for letter, index in self._yellow_chars:
            if word[index] == letter or letter not in word:
                return False
        return True

    def __contains_green_chars(self, word):
        for letter, index in self._green_chars:
            if word[index] != letter:
                return False
        return True

    def _remove_invalid_words(self):
        new_candidates = []
        for word in self._possible_words:
            if self.__contains_invalid_chars(word) or not self.__contains_yellow_chars(word) or not self.__contains_green_chars(word):
                continue
            new_candidates.append(word)
        self._possible_words = new_candidates

    def _make_educated_guess(self):
        untried_letters, freq_map = self.__get_probability_scores(self._possible_words)
        if len(untried_letters) > 1 and self.attempts <= ATTEMPT_LIMIT - 1:
            word_with_score = []
            word_list = self._possible_words
            for word in word_list:
                letters = set(word)
                untried_score = sum(untried_letters[c] if c in untried_letters else 0 for c in letters)
                freq_score = sum(freq_map[c] for c in letters)
                word_with_score.append((word, untried_score, freq_score))
            ranked_words = sorted(word_with_score, key=lambda item: (-item[1], -item[2], item[0]))
            guess = ranked_words[0][0]
        else:
            guess = sorted(self._possible_words, key=lambda word: (-len(set(word)), -sum(freq_map[c] for c in word), word))[0]
        return guess

    def _next_guess(self):
        self._remove_invalid_words()
        if len(self._possible_words) == 0:
            return None
        elif len(self._possible_words) == 1:
            return self._possible_words[0]
        return self._make_educated_guess()

    def solve(self, wordle, debug=False):
        while self.attempts<ATTEMPT_LIMIT:
            self.attempts += 1
            guess = self._next_guess()
            self.tries.append(guess)
            if debug:
                print(guess)
            status, result = wordle.check_answer(guess)
            if status == GameResult.WON:
                return True, self.attempts
            elif status == GameResult.LOST:
                return False, self.attempts
            elif status == GameResult.FAILED_ATTEMPT:
                for i, (c, r) in enumerate(zip(guess, result)):
                    self._untried_chars.discard(c)
                    if r == GuessResult.GREEN:
                        self._green_chars.add((c, i))
                        if c in self._yellow_chars:
                            self._yellow_chars.remove((c, i))
                    elif r == GuessResult.YELLOW:
                        self._yellow_chars.add((c, i))
                    elif r == GuessResult.BLACK:
                        self._invalid_chars.add(c)
            elif status == GameResult.INVALID_WORD:
                self.attempts -= 1
                self._possible_words.remove(guess)
                self._all_possible_words.remove(guess)
                        
        
