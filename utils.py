from enum import Enum

LETTER_COUNT = 5
ATTEMPT_LIMIT = 6

class GameResult:
    LOST = 0
    WON = 1
    FAILED_ATTEMPT = 2
    INVALID_TRY = 3
    INVALID_WORD = 4

class CharResult:
    GREEN = 'g'
    YELLOW = 'y'
    BLACK = 'b'

def dictionary():
    with open("/usr/share/dict/words", "r") as word_file:
        return sorted([word.strip().lower() for word in word_file.readlines() if len(word.strip()) == LETTER_COUNT])

def wordle_words():
    with open("all_wordle_words.txt", "r") as infile:
        return [line.strip() for line in infile.readlines()]