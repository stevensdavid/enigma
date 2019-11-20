from random import randrange
from functools import reduce
from typing import Iterable

ALPHABET = list(map(chr, range(ord('A'),ord('Z')+1)))

class RotorGroup:
    def __init__(self, rotors: list(int)):
        self.rotors = [Rotor(x) for x in rotors]

    def transform(self, letter: str, forward:bool =True) -> str:
        if forward:
            r1, r2, r3 = self.rotors
            r1.increment()
            if r1.step in r1.turnover_points:
                r2.increment()
                if r2.step in r2.turnover_points:
                    r3.increment()
            return reduce(lambda r, l: r.transform(l), self.rotors, letter)
        else:
            return reduce(lambda r, l: r.transform(l), reversed(self.rotors), letter)

    def choose_rotors(self, *rotors: Iterable(int)) -> None:
        self.rotors = [Rotor(x) for x in rotors]


class Rotor:
    def __init__(self, number: int):
        self.encrypt = {}
        self.turnover_points = []
        self.step = 'A'

        self.change_rotor(number)

    def change_rotor(self, number: int):
        encryption = {
            1: 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 
            2: 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
            3: 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
            4: 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
            5: 'VZBRGITYUPSDNHLXAWMJQOFECK',
            6: 'JPGVOUMFYQBENHZRDKASXLICTW',
            7: 'NZJHGRCXMYSWBOUFAIVLPEKQDT',
            8: 'FKQHTLXOCBJSPDZRAMEWNIUYGV'
        }
        self.encrypt = {k:v for k,v in zip(ALPHABET, encryption[number])}
        turnovers = {
            1:['Q'],
            2:['E'],
            3:['V'],
            4:['J'],
            5:['Z']
        }.update({n:['Z','M'] for n in (6,7,8)})
        self.turnover_points = turnovers[number]

    def increment(self) -> None:
        # 'A' is 65 in ASCII, 26 letters in alphabet
        self.step = chr(((ord(self.step) - 65 + 1) % 26) + 65)

    def transform(self, letter: str) -> str:
        return self.encrypt[letter]

class Plugboard:
    def __init__(self, mapping=None):
        letters: list(str) = ALPHABET
        if mapping:
            self.steckerbrett = mapping
        else:
            # Default to random mapping
            self.steckerbrett = {}
            while len(letters) > 0:
                x = randrange(0, len(letters))
                a = letters.pop(x)
                y = randrange(0, len(letters))
                b = letters.pop(y)
                self.steckerbrett[a], self.steckerbrett[b] = b, a

    def set_plugboard(self, mapping: dict(str,str)) -> None:
        self.steckerbrett = mapping

    def transform(self, letter:str) -> str:
        return self.steckerbrett[letter]

class Reflector(Plugboard):
    def __init__(self, **kwargs):
        super(Reflector, self).__init__(**kwargs)

    def set_reflector(self, mapping: dict(str, str)) -> None:
        self.set_plugboard(mapping)
    

class EnigmaMachine:
    def __init__(self):
        self.plugboard = Plugboard()
        self.rotor_group = RotorGroup([1,2,3])
        self.reflector = Reflector()

    def transform(self, letter: str) -> str:
        sequence = [
            self.plugboard.transform, 
            lambda l: self.rotor_group.transform(l, forward=True), 
            self.reflector.transform, 
            lambda l: self.rotor_group.transform(l, forward=False), 
            self.reflector.transform
        ]
        return reduce(lambda l, f: f(l), sequence, letter)

    def set_rotors(self, rotor1: int, rotor2: int, rotor3: int) -> None:
        self.rotor_group.choose_rotors(rotor1, rotor2, rotor3)


if __name__ == "__main__":
    enigma = EnigmaMachine()
    result = ''.join(map(enigma.transform, 'hello'))
    print(result)
