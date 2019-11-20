from random import randrange
from functools import reduce

ALPHABET = list(map(chr, range(ord('A'),ord('Z')+1)))

class RotorGroup:
    def __init__(self, rotors: list(int)):
        self.rotors = [Rotor(x) for x in rotors]

    def transform(self, forward=True):
        if forward:
            pass
        else:
            pass


class Rotor:
    def __init__(self, number: int):
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
        self.step = 0

        turnovers = {
            1:['Q'],
            2:['E'],
            3:['V'],
            4:['J'],
            5:['Z']
        }.update({n:['Z','M'] for n in (6,7,8)})
        self.turnover_character = turnovers[number]

    def increment(self):
        self.step = (self.step + 1) % 26

    def transform(self, letter: str) -> str:
        pass

class Plugboard:
    def __init__(self):
        letters: list(str) = ALPHABET
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

class Reflector:
    def __init__(self):
        pass

    def transform(self, letter: str) -> str:
        pass
    
class EnigmaMachine:
    def __init__(self):
        self.plugboard = Plugboard()
        self.rotor_group = RotorGroup([])
        self.reflector = Reflector

    def transform(self, letter: str) -> str:
        sequence = [
            self.plugboard.transform, 
            self.rotor_group.transform(forward=True), 
            self.reflector.transform, 
            self.rotor_group.transform(forward=False), 
            self.reflector.transform
        ]
        return reduce(lambda l, f: f(l), sequence, letter)

    def set_rotors(self, rotor1, rotor2, rotor3):
        pass

if __name__ == "__main__":
    enigma = EnigmaMachine()
    result = ''.join(map(enigma.transform, 'hello'))
    print(result)
