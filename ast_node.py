from abc import abstractmethod
from dataclasses import dataclass


@dataclass
class LispElement:
    @abstractmethod
    def is_atom(self):
        pass

    def __eq__(self, other):
        return type(self) == type(other)


class LispList(list, LispElement):
    def is_atom(self) -> bool:
        return len(self) == 0

    def __str__(self):
        return f'({" ".join(map(str, self))})'

    def __eq__(self, other):
        return LispElement.__eq__(self, other) and list.__eq__(self, other)


@dataclass
class LispAtom(LispElement):
    literal: str

    def is_atom(self) -> bool:
        return True

    def __str__(self):
        return self.literal

    def __eq__(self, other):
        return super().__eq__(other) and self.literal == other.literal


@dataclass
class LispNumber(LispAtom):
    number: int

    def __str__(self):
        return str(self.number)

    def __eq__(self, other):
        return LispElement.__eq__(self, other) and self.number == other.number


class LispString(str, LispAtom):

    def __eq__(self, other):
        return LispElement.__eq__(self, other) and str.__eq__(self, other)
