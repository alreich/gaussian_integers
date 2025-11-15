from abc import ABC, abstractmethod
from fractions import Fraction

import generic_utils as utils

class CayleyDicksonBase(ABC):
    """An Abstract Base Class (ABC) for subclasses that implement the Cayley-Dickson construction.
    This class cannot be instantiated directly. All instances of this class are immutable.
    Also, all instances of this class have only TWO components, each one consisting of a number
    of some type (e.g., integer, Fraction) or another instance of CayleyDicksonBase subclass.
    """

    # See the Fano plane figure at https://en.wikipedia.org/wiki/Octonion
    # The default list of case-sensitive unit strings, below, corresponds to
    # the notation in that figure as follows:
    # 1 = real part,     L = e_4 (L)
    # i = e_1 (I),       I = e_5 (IL)
    # j = e_2 (J),       J = e_6 (JL)
    # k = e_3 (IJ),      K = e_7 (IJL)
    _default_unit_strings = ["1", "i", "j", "k", "L", "I", "J", "K"]
    unit_strings = utils.ResettableValue(_default_unit_strings)

    _alternative_unit_strings = ["1", "I", "J", "IJ", "L", "IL", "JL", "IJL"]

    _use_scalar_mult: bool = False
    _include_zero_coefs: bool = False

    def __init__(self, real=None, imag=None):
        self._re = real
        self._im = imag

    @property
    def real(self):
        return self._re

    @property
    def imag(self):
        return self._im

    @classmethod
    def use_scalar_mult(cls, value=None):
        if value is None:
            return cls._use_scalar_mult
        elif isinstance(value, bool):
            cls._use_scalar_mult = value
            return value
        else:
            raise ValueError("Value must be None or a Boolean")

    @classmethod
    def include_zero_coefs(cls, value=None):
        if value is None:
            return cls._include_zero_coefs
        elif isinstance(value, bool):
            cls._include_zero_coefs = value
            return cls._include_zero_coefs
        else:
            raise ValueError("Value must be None or a Boolean")

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

    # def generate_unit_strings(value=None, prefix=None, size=None):
    #     """
    #     value -- Custom, user-provided list of unit strings
    #     prefix - Prefix to use for each element, if generating unit strings
    #     size --- Number of unit strings to generate
    #     """
    #
    #     if value is None:
    #
    #         # No changes; output current list of unit strings
    #         if prefix is None and size is None:
    #             pass
    #
    #         # Create generic list of unit strings, e.g., 'e1', 'e2', 'e3', ...
    #         elif isinstance(prefix, str) and isinstance(size, int) and size > 0:
    #             count = 1
    #             generic_list = ['1']
    #             for x in range(size - 1):
    #                 generic_list.append(prefix + str(count))
    #                 count += 1
    #             result = generic_list
    #         else:
    #             raise TypeError(f"Inconsistent inputs")
    #
    #     # Use a custom, user-provided list of unit strings
    #     elif isinstance(value, list):
    #         result = value
    #
    #     # Reset the list of unit strings to their default value
    #     elif isinstance(value, bool) and value:
    #         result = cls._default_unit_strings  # Reset to default
    #
    #     else:
    #         raise TypeError(f"inputs inconsistent")
    #
    #     return result

    @property
    def order(self):
        """Order is the number levels contained in the Zi.
        That is, a Zi made up of two integers has order 1, and a Zi
        made up of two other Zi's, each of order n, has order n+1."""
        def aux(x, d):
            if isinstance(x, (int, float, complex, Fraction)):
                return d
            else:
                return aux(x.real, d + 1)
        return aux(self.real, 1)

    @property
    def dim(self):
        """Dimension is the total number of numbers making up this Zi.
        So, if n is its order, then its dimension is 2^n."""
        return 2 ** self.order

    @property
    def first(self):
        """Return the first re value."""
        if isinstance(self.real, (int, float, complex, Fraction)):
            return self.real
        elif isinstance(self.real, CayleyDicksonBase):
            return self.real.first
        else:
            raise Exception(f"Cannot create a real from {self}")

    @abstractmethod
    def conjugate(self):
        pass

    @property
    def norm(self):
        return (self * self.conjugate()).first

    def to_array(self):
        re, im = self
        if isinstance(re, (float, int)) and isinstance(im, (float, int)):
            return [re, im]
        elif isinstance(re, CayleyDicksonBase) and isinstance(im, CayleyDicksonBase):
            return [re.to_array(), im.to_array()]
        else:
            raise Exception(f"Cannot create an array from {self}")

    @property
    def is_real(self):
        if isinstance(self.real, (int, float, complex, Fraction)) and self.imag == 0:
            return self.real
        else:
            return False

    @property
    def is_complex(self):
        """Return True if this Zi is essentially a complex number
        That is, the re & im parts are numbers, not other Zis."""
        return self.order == 1

    @property
    def is_quaternion(self):
        """Return True if this Zi is essentially a quaternion
        That is, the re & im parts are essentially complex numbers."""
        return self.order == 2

    @property
    def is_octonion(self):
        """Return True if this Zi is essentially an octonion
        That is, the re & im parts are essentially quaternions."""
        return self.order == 3

    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __sub__(self, other):
        pass

    @abstractmethod
    def __mul__(self, other):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __abs__(self):
        pass

    @abstractmethod
    def __neg__(self):
        pass

    @abstractmethod
    def __pos__(self):
        pass

    @staticmethod
    def from_array(arr):
        pass

    # @abstractmethod
    # def __pow__(self, n: int):
    #     pass

