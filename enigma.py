from random import randrange
from typing import Iterable, List, Dict

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class RotorGroup:
    def __init__(self, rotors: List[int], ringstellung: List[int]):
        self.rotors = self.choose_rotors(rotors, ringstellung)

    def transform(self, letter: str, forward: bool = True) -> str:
        if forward:
            self.increment_right()
            for rotor in reversed(self.rotors):
                # Forward transformation is applied from right to left
                letter = rotor.transform(letter, forward)
            return letter
        else:
            for rotor in self.rotors:
                letter = rotor.transform(letter, forward)
            return letter

    def increment_right(self):
        _, middle, right = self.rotors
        if (right.step in right.turnover_points 
            or middle.step in middle.turnover_points):
            # second clause is double step
            self.increment_middle()
        right.increment()

    def increment_middle(self):
        middle = self.rotors[1]
        if middle.step in middle.turnover_points:
            self.increment_left()
        middle.increment()

    def increment_left(self):
        self.rotors[0].increment()

    def choose_rotors(self, rotors: List[int], 
                      ringstellung: List[int] = None) -> None:
        if ringstellung is None:
            ringstellung = [0, 0, 0]
        return [Rotor(r, s) for r, s in zip(rotors, ringstellung)]

    def increment_rotor(self, rotor: str) -> str:
        if rotor == 'right':
            r = self.rotors[2]
        elif rotor == 'middle':
            r = self.rotors[1]
        elif rotor == 'left':
            r = self.rotors[0]
        r.increment()
        return r.step

    def rotor_position(self, rotor: str) -> str:
        if rotor == 'left':
            idx = 0
        elif rotor == 'middle':
            idx = 1
        elif rotor == 'right':
            idx = 2
        return self.rotors[idx].step

    def rotor_positions(self) -> List[str]:
        return list(map(lambda x: x.step, self.rotors))


class Rotor:
    def __init__(self, number: int, ringstellung: int):
        self.encrypt = {}
        self.turnover_points = []
        self.step = 'A'
        self.type = number
        # change ringstellung to zero-indexed
        self.ringstellung = ringstellung - 1

        self.change_rotor(number, ringstellung)

    def change_rotor(self, number: int, ringstellung):
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
        selected_enc = encryption[number]
        self.encrypt = {k: v for k, v in zip(ALPHABET, selected_enc)}
        self.reverse_encrypt = {v: k for k, v in self.encrypt.items()}
        turnovers = {
            1: ['Q'],
            2: ['E'],
            3: ['V'],
            4: ['J'],
            5: ['Z']
        }
        # Add later 6,7,8 rotor versions
        turnovers.update({n: ['Z', 'M'] for n in (6, 7, 8)})
        self.turnover_points = turnovers[number]

    def increment(self) -> None:
        # 'A' is 65 in ASCII, 26 letters in alphabet
        self.step = chr(((ord(self.step) - 65 + 1) % 26) + 65)

    def transform(self, letter: str, forward: bool) -> str:
        offset_letter = chr(
            (
                ord(letter) + ord(self.step) - self.ringstellung - 2*65
            ) % 26 + 65
        )
        if forward:
            transformed = self.encrypt[offset_letter]
        else:
            transformed = self.reverse_encrypt[offset_letter]
        offset = chr((
            ord(transformed) - ord(self.step) + self.ringstellung - 2*65
        ) % 26 + 65)
        return offset


class Plugboard:
    def __init__(self, mapping: Dict[str, str]):
        reflected_mapping = {v: k for k, v in mapping.items()}
        mapping.update(reflected_mapping)
        self.steckerbrett = mapping

    def set_mapping(self, mapping: Dict[str, str]) -> None:
        self.steckerbrett = mapping

    def transform(self, letter: str) -> str:
        return (self.steckerbrett[letter] 
                if letter in self.steckerbrett 
                else letter)


class Reflector(Plugboard):
    def __init__(self, reflector_type):
        if reflector_type == 'B':
            ukw = {k: v for k, v in zip(
                ALPHABET, 'YRUHQSLDPXNGOKMIEBFZCWVJAT')}
        elif reflector_type == 'C':
            ukw = {k: v for k, v in zip(
                ALPHABET, 'FVPJIAOYEDRZXWGCTKUQSBNMHL')}
        else:
            raise ValueError('Only type B and C are supported')
        super(Reflector, self).__init__(mapping=ukw)


class EnigmaMachine:
    def __init__(self, pb_map: Dict[str, str], reflector: str,
                 rotors: List[int], ringstellung: List[int]):
        self._pb_map = pb_map
        self._reflector = reflector
        self._rotors = rotors
        self._ringstellung = ringstellung

        self.plugboard = Plugboard(pb_map)
        self.rotor_group = RotorGroup(rotors, ringstellung)
        self.reflector = Reflector(reflector)

    def encrypt_message(self, msg: str) -> str:
        """Encrypt the message

        Examples
        --------
        The famous Operation Barbarossa message's first part:
        >>> plugboard_map = { 'A': 'V', 'B': 'S', 'C': 'G', 'D': 'L', 
        ... 'F': 'U', 'H': 'Z', 'I': 'N', 'K': 'M', 'O': 'W', 'R': 'X' }
        >>> rotors = [2, 4, 5]
        >>> ringstellung = [2, 21, 12]
        >>> enigma = EnigmaMachine(pb_map=plugboard_map, reflector='B', 
        ... rotors=rotors, ringstellung=ringstellung)
        >>> while enigma.rotor_position('right') != 'A':
        ...     _ = enigma.increment_rotor('right')
        ...
        >>> while enigma.rotor_position('middle') != 'L':
        ...     _ = enigma.increment_rotor('middle')
        ...
        >>> while enigma.rotor_position('left') != 'B':
        ...     _ = enigma.increment_rotor('left')
        ...
        >>> from copy import copy
        >>> e = copy(enigma)
        >>> e.encrypt_message('EDPUD NRGYS ZRCXN UYTPO MRMBO FKTBZ ' +
        ... 'REZKM LXLVE FGUEY SIOZV EQMIK UBPMM YLKLT TDEIS MDICA ' + 
        ... 'GYKUA CTCDO MOHWX MUUIA UBSTS LRNBZ SZWNR FXWFY SSXJZ ' +
        ... 'VIJHI DISHP RKLKA YUPAD TXQSP INQMA TLPIF SVKDA SCTAC ' + 
        ... 'DPBOP VHJK')
        'AUFKLXABTEILUNGXVONXKURTINOWAXKURTINOWAXNORDWESTLXSEBEZXSEBEZX\
UAFFLIEGERSTRASZERIQTUNGXDUBROWKIXDUBROWKIXOPOTSCHKAXOPOTSCHKAXUMXEINSA\
QTDREINULLXUHRANGETRETENXANGRIFFXINFXRGTX'
        >>> e = copy(enigma)
        >>> e.encrypt_message('AUFKLXABTEILUNGXVONXKURTINOWAXKURTINOW' +
        ... 'AXNORDWESTLXSEBEZXSEBEZXUAFFLIEGERSTRASZERIQTUNGXDUBROWK' +
        ... 'IXDUBROWKIXOPOTSCHKAXOPOTSCHKAXUMXEINSAQTDREINULLXUHRANG' +
        ... 'ETRETENXANGRIFFXINFXRGTX')
        'EDPUDNRGYSZRCXNUYTPOMRMBOFKTBZREZKMLXLVEFGUEYSIOZVEQMIKUBPMMYL\
KLTTDEISMDICAGYKUACTCDOMOHWXMUUIAUBSTSLRNBZSZWNRFXWFYSSXJZVIJHIDISHPRKL\
KAYUPADTXQSPINQMATLPIFSVKDASCTACDPBOPVHJK'
        """
        return ''.join(map(self.encrypt, msg.replace(' ', '').upper()))

    def encrypt(self, letter: str) -> str:
        sequence = [
            self.plugboard.transform,
            lambda l: self.rotor_group.transform(l, forward=True),
            self.reflector.transform,
            lambda l: self.rotor_group.transform(l, forward=False),
            self.plugboard.transform
        ]
        for f in sequence:
            letter = f(letter)
        return letter

    def set_rotors(self, rotor1: int, rotor2: int, rotor3: int) -> None:
        self.rotor_group.choose_rotors([rotor1, rotor2, rotor3])

    def set_reflector(self, mapping: Dict[str, str]) -> None:
        self.reflector.set_mapping(mapping)

    def set_plugboard(self, mapping: Dict[str, str]) -> None:
        self.plugboard.set_mapping(mapping)

    def increment_rotor(self, rotor: str) -> str:
        return self.rotor_group.increment_rotor(rotor)

    def rotor_position(self, rotor: str) -> str:
        return self.rotor_group.rotor_position(rotor)

    def rotor_positions(self) -> List[str]:
        return self.rotor_group.rotor_positions()

    def __copy__(self):
        other = EnigmaMachine(self._pb_map, self._reflector,
                              self._rotors, self._ringstellung)
        while other.rotor_position('right') != self.rotor_position('right'):
            other.increment_rotor('right')
        while other.rotor_position('middle') != self.rotor_position('middle'):
            other.increment_rotor('middle')
        while other.rotor_position('left') != self.rotor_position('left'):
            other.increment_rotor('left')
        return other


if __name__ == "__main__":
    import doctest
    doctest.testmod()
