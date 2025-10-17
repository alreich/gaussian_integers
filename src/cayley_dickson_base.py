from abc import ABC, abstractmethod
from fractions import Fraction

class CayleyDicksonBase(ABC):
    """An Abstract Base Class (ABC) for subclasses that implement the Cayley-Dickson construction.
    This class cannot be instantiated directly. All instances of this class are immutable.
    Also, all instances of this class have only TWO components, each one consisting of a number
    of some type (e.g., integer, Fraction) or another instance of CayleyDicksonBase subclass.
    """

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
        if isinstance(self.real, (int, float, complex, Fraction)):
            return f"{self.__class__.__name__}({self.real}, {self.imag})"
        else:
            return f"{self.__class__.__name__}({repr(self.real)}, {repr(self.imag)})"

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

    def to_array(self):
        re, im = self
        if isinstance(re, (float, int)) and isinstance(im, (float, int)):
            return [re, im]
        elif isinstance(re, CayleyDicksonBase) and isinstance(im, CayleyDicksonBase):
            return [re.to_array(), im.to_array()]
        else:
            raise Exception(f"Cannot create an array from {self}")

    # @abstractmethod
    # def __str__(self):
    #     pass

    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __sub__(self, other):
        pass

    # @abstractmethod
    # def __mul__(self, other):
    #     pass
    #
    # @abstractmethod
    # def __pow__(self, n: int):
    #     pass
    #
    # @abstractmethod
    # def __abs__(self):
    #     pass
    #
    # @abstractmethod
    # def __neg__(self):
    #     pass
    #
    # @abstractmethod
    # def __pos__(self):
    #     pass
    #
    # @abstractmethod
    # def __norm__(self):
    #     pass
    #
    # @abstractmethod
    # def from_array(self, array):
    #     pass
    #
    # @abstractmethod
    # def order(self) -> int:
    #     pass



