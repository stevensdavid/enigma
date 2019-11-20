from random import randrange
from functools import reduce

class Rotor:
    def __init__(self):
        self.step = 0

    def increment(self):
        self.step = (self.step + 1) % 26

    def transform(self, letter: str) -> str:
        pass

class Plugboard:
    def __init__(self):
        letters: list(str) = [chr(x) for x in range(ord('A'),ord('Z')+1)]
        self.steckerbrett = {}
        while len(letters) > 0:
            x = randrange(0, len(letters))
            a = letters.pop(x)
            y = randrange(0, len(letters))
            b = letters.pop(y)
            self.steckerbrett[a], self.steckerbrett[b] = b, a
        print(self.steckerbrett)

    def transform(self, letter:str) -> str:
        pass
    
class EnigmaMachine:
    def __init__(self):
        self.plugboard = Plugboard()
        self.rotors = []

    def transform(self, letter: str) -> str:
        sequence = [self.plugboard.transform] + list(map(lambda r: r.transform, self.rotors)) + [self.plugboard.transform]
        return reduce(lambda l, f: f(l), sequence, letter)

    def set_rotors(self, rotor1, rotor2, rotor3):
        pass

if __name__ == "__main__":
    enigma = EnigmaMachine()
    result = ''.join(map(enigma.transform, 'hello'))
    print(result)
