from enum import Enum


class LetterState(Enum):
    NOT_USED = "NOT_USED"
    RIGHT_POSTION = "RIGHT_POSTION"
    WRONG_POSITION = "WRONG_POSITION"
    NONE = "NONE"


class Letter:
    def __init__(self, char, position=-1, state=LetterState.NONE):
        self.char = char.upper()
        self.position = position
        self.state = state

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
    print(letters[i])


words = []

with open('../data/words.txt', 'r') as file:
    for word in file:
        words.append(Word(word.strip(), 0))

############## TUDO INICIALIZADO #################################
# calcular a entropia, e pegar a palavra que da mais informacao
