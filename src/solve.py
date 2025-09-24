from enum import Enum
from collections import Counter
import math
import sys


path = "./data/words.txt"
if len(sys.argv) == 1:
    print(f"using path = {
          path}\nif u want to use another path please pass by argument")
else:
    path = sys.argv[1]


class LetterState(Enum):
    NOT_USED = "NOT_USED"
    RIGHT_POSTION = "RIGHT_POSTION"
    WRONG_POSITION = "WRONG_POSITION"
    NONE = "NONE"


class PatternState(Enum):
    GREEN = "GREEN"
    YELLOW = "YELLOW"
    GRAY = "GRAY"


class Pattern:
    def __init__(self, states):
        assert (len(states) == 5)
        self.states = states

    def __repr__(self):
        return f"{self.states[0]} {self.states[1]} {self.states[2]} {self.states[3]} {self.states[4]}"


class Letter:
    def __init__(self, char, position=-1, state=LetterState.NONE):
        self.char = char.upper()
        self.position = position
        self.state = state
        self.possible_positions = [0, 1, 2, 3, 4]

    def __repr__(self):
        return f"Letter(char='{self.char}', position={self.position}, state={self.state.name})"


class Word:
    def __init__(self, word, self_info):
        self.word = word
        self.self_info = self_info

    def __repr__(self):
        return f"Word(word={self.word}, info={self.self_info})"


letters = []
for i in range(0, 26):
    letters.append(Letter(chr(ord('a') + i)))
   # print(letters[i])


words = []

with open(path, 'r') as file:
    for word in file:
        words.append(Word(word.strip(), 0))

patterns = []
patterns_size = 3**5
for i in range(0, patterns_size):
    tmp = i
    p = [PatternState.GREEN] * 5
    for j in range(0, 5):
        if tmp % 3 == 2:
            p[j] = PatternState.GREEN
        if tmp % 3 == 1:
            p[j] = PatternState.YELLOW
        if tmp % 3 == 0:
            p[j] = PatternState.GRAY
        tmp = tmp // 3
    patterns.append(Pattern(p))
    # print(patterns[i])


############## TUDO INICIALIZADO #################################
# calcular a entropia, e pegar a palavra que da mais informacao
# pi = probabilidade do padrao i dado a palavra x
# -sum(pi * log2(pi))


def get_pattern_given_answer(guess, answer):
    pattern = [PatternState.GRAY] * 5
    used = [False] * 5

    for i in range(5):
        if guess[i] == answer[i]:
            pattern[i] = PatternState.GREEN
            used[i] = True

    for i in range(5):
        if pattern[i] == PatternState.GREEN:
            continue

        for j in range(5):
            if not used[j] and guess[i] == answer[j]:
                pattern[i] = PatternState.YELLOW
                used[j] = True
                break

    return Pattern(pattern)


# p(word | pat) = numero de palavras que fazem o padrao pat se eu colocasse word
#                                  palavras restantes
def calculate_entropy(word):
    pattern_freq = Counter()
    for answer in words:
        pat = get_pattern_given_answer(word.word, answer.word)
        pattern_freq[tuple(pat.states)] += 1

    entropy = 0
    for pat in patterns:
        pi = pattern_freq[tuple(pat.states)] / len(words)
        if pi == 0:
            continue
        entropy += pi * math.log2(pi)

    return -entropy


def parse_pattern(pattern_input):
    ret_pat = [PatternState.GRAY] * 5

    for i in range(5):
        if (pattern_input[i].upper() == 'G'):
            ret_pat[i] = PatternState.GREEN
        if (pattern_input[i].upper() == 'Y'):
            ret_pat[i] = PatternState.YELLOW
        if (pattern_input[i].upper() == 'B'):
            ret_pat[i] = PatternState.GRAY

    return Pattern(ret_pat)


def filter_words(words, guess, pattern):
    ret = []
    for w in words:
        if (get_pattern_given_answer(guess.word, w.word).states == pattern.states):
            ret.append(w)
    return ret


all_words = words.copy()

skip_first = True
while (len(words) > 1):
    print(f"size: {len(words)}")

    # update words
    if skip_first:
        guess_input = input("Enter your guess word: ").strip().lower()
        pattern_input = input("Enter the resulting pattern (G/Y/B): ").strip()
        assert (len(pattern_input) == 5)

        pattern = parse_pattern(pattern_input)
        words = filter_words(words, Word(guess_input, 0), pattern)

    assert (len(words) > 0)

    for word in words:
        entropy = calculate_entropy(word)
        word.self_info = entropy
        # print(f"word {word.word}, entropy: {entropy}")

    for word in all_words:
        entropy = calculate_entropy(word)
        word.self_info = entropy

    words.sort(key=lambda w: w.self_info, reverse=True)
    print("Possible answers")
    for w in words[:5]:
        print(w)

    all_words.sort(key=lambda w: w.self_info, reverse=True)
    print("All words")
    for w in all_words[:5]:
        print(w)

    skip_first = True

print(words[0])
