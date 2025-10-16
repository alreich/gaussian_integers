from abc import ABC  #, abstractmethod

class CayleyDicksonBase(ABC):
    """The base class for subclasses the implement the Cayley-Dickson construction."""

    def __init__(self, real=None, imag=None):
        self._re = real
        self._im = imag

    @property
    def real(self):
        return self._re

    @property
    def imag(self):
        return self._im

    def __repr__(self):
        return f"{self.__class__.__name__}({self.real}, {self.imag})"

    def __hash__(self):
        return hash((self.real, self.imag, type(self)))

    def __len__(self):
        return 2

    def __getitem__(self, index):
        if isinstance(index, int):
            if index == 0:
                return self.real
            elif index == 1:
                return self.imag
            else:
                raise IndexError(f"Index {index} out of range")
        else:
            raise TypeError(f"Index {index} must be a non-negative integer")

    def __iter__(self):
        return iter((self.real, self.imag))

    def __eq__(self, other):
        if type(self) == type(other):
            return self.real == other.real and self.imag == other.imag
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
