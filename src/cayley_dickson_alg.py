# This is Work-In-Progress

from random import randint
from math import sqrt
from numbers import Number

def flatten(list_of_lists):
    return [item for lst in list_of_lists for item in lst]

class Zi:
    """Pairs of integers (Gaussian Integers), pairs of Gaussian integers (Quaternion Integers),
    and pairs of Quaternion integers (Octonion Integers), etc."""

    def __init__(self, re=None, im=None):

        # --------------------------------------------------------
        # re is a float or int, and im is a float, int, or None

        if isinstance(re, (float, int)):
            self.__re = round(re)
            if im is None:
                self.__im = 0
            elif isinstance(im, (float, int)):
                self.__im = round(im)
            else:
                raise Exception(f"Inputs incompatible: {re} and {im}")

        # --------------------------------------------------------
        # re is a complex, and im is None, a complex, or a Zi

        elif isinstance(re, complex):
            if im is None:  #
                self.__re = round(re.real)
                self.__im = round(re.imag)
            elif isinstance(im, (complex, Zi)):
                self.__re = Zi(re)
                self.__im = Zi(im)
            else:
                raise Exception(f"Inputs incompatible: {re} and {im}")

        # --------------------------------------------------------
        # re is a Zi, and im is None, a complex, or a Zi

        elif isinstance(re, Zi):
            if im is None:
                self.__re = re.real
                self.__im = re.imag
            elif isinstance(im, (complex, Zi)):
                self.__re = Zi(re)
                self.__im = Zi(im)
            else:
                raise Exception(f"Inputs incompatible: {re} and {im}")

        # --------------------------------------------------------
        # Both re and im are None

        elif re is None:
            self.__re = 0
            if im is None:
                self.__im = 0
            else:
                raise Exception(f"If re is None, then im must be None. But im = {im}")
        else:
            raise Exception(f"Unexpected combination of input types: {re} and {im}")

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.__re)}, {repr(self.__im)})"

    def __str__(self):
        if self.is_complex():
            return str(complex(self))
        elif self.is_quaternion():
            return self.quaternion_to_string()
        elif self.is_octonion():
            return f"Oct({str(self.__re)}, {str(self.__im)})"
        else:
            return str(self.to_array())

    def __neg__(self):
        return Zi(- self.__re, - self.__im)

    def __add__(self, other):
        return Zi(self.__re + other.real, self.__im + other.imag)

    def __radd__(self, other):
        """The reflected (swapped) operand for addition: other + self"""
        return Zi(other) + self

    def __iadd__(self, other):
        """Implements the += operation: self += other"""
        return Zi(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return Zi(self.__re - other.real, self.__im - other.imag)

    def __rsub__(self, other):
        """The reflected (swapped) operand for subtraction: other - self"""
        return Zi(other) - self

    def __isub__(self, other):
        """Implements the -= operation: self -= other"""
        return Zi(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        """
        Cayley-Dickson Construction -- see [Schafer, 1966]

        Conjugation, denoted here by *, is defined recursively as:
        a* = a and (u, v)* = (u*, -v)

        Multiplication is also defined recursively as:
        (a, b) x (c, d) = (a x c  +  mu x d x b*, a* x d  +  c x b)
        where for now, mu = -1 is implicitly hardcoded, below.
        """
        a, b, c, d = self.__re, self.__im, other.real, other.imag
        real_part = a * c - d * b.conjugate()
        imag_part = a.conjugate() * d + c * b
        return Zi(real_part, imag_part)

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        """Implements the *= operation: self *= other"""
        a = self.real
        b = self.imag
        c = round(other.real)
        d = round(other.imag)
        return Zi(a * c - b * d, a * d + b * c)

    def __complex__(self):
        depth = self.depth()
        if depth == 0:
            return complex(self.__re, self.__im)
        else:
            raise Exception(f"Cannot create a complex from {self}")

    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise AttributeError(f"Zi's are immutable. Cannot modify {name}")
        super().__setattr__(name, value)

    @property
    def real(self):
        return self.__re

    @property
    def imag(self):
        return self.__im

    @property
    def first(self):
        """Return the innermost first re value."""
        if isinstance(self.__re, int):
            return self.__re
        else:
            return self.__re.first

    @property
    def norm(self):
        return (self * self.conjugate()).first

    def conjugate(self):
        """This definition works recursively."""
        return Zi(self.__re.conjugate(), - self.__im)

    def depth(self):
        """Depth is the number levels contained in the Zi.
        That is, a Zi made up of two integers has depth 0, and a Zi
        made up of two other Zi's, each of depth n, has depth n+1."""
        def aux(x, d):
            if isinstance(x, int):
                return d
            else:
                return aux(x.real, d + 1)
        return aux(self.__re, 0)

    def is_complex(self):
        """Return True if this Zi is essentially a complex number
        That is, the re & im parts are numbers, not other Zis."""
        return self.depth() == 0

    def is_quaternion(self):
        """Return True if this Zi is essentially a quaternion
        That is, the re & im parts are essentially complex numbers."""
        return self.depth() == 1

    def is_octonion(self):
        """Return True if this Zi is essentially an octonion
        That is, the re & im parts are essentially quaternions."""
        return self.depth() == 2

    def to_array(self):
        if isinstance(self.__re, (float, int)) and isinstance(self.__im, (float, int)):
            return [self.__re, self.__im]
        elif isinstance(self.__re, Zi) and isinstance(self.__im, Zi):
            return [self.__re.to_array(), self.__im.to_array()]
        else:
            raise Exception(f"Cannot create an array from {self}")

    @staticmethod
    def from_array(arr):
        re = arr[0]
        im = arr[1]
        if isinstance(re, int) and isinstance(im, int):
            return Zi(re, im)
        else:
            return Zi(Zi.from_array(re), Zi.from_array(im))

    def quaternion_to_string(self):
        unit_strs = ["", "i", "j", "k"]
        if self.is_quaternion():
            qstr = "Quat("
            for idx, coef in enumerate(flatten(self.to_array())):
                if coef > 0:
                    qstr = qstr + f"+{coef}{unit_strs[idx]}"
                elif coef < 0:
                    qstr = qstr + f"{coef}{unit_strs[idx]}"
                else:
                    pass
            return qstr + ")"
        else:
            raise Exception(f"{self} is not a quaternion")

    @staticmethod
    def random(re1=-100, re2=100, im1=-100, im2=100, depth=0):
        if depth == 0:
            return Zi(randint(re1, re2), randint(im1, im2))
        else:
            d = depth - 1
            return Zi(Zi.random(re1, re2, im1, im2, d),
                      Zi.random(re1, re2, im1, im2, d))

    @staticmethod
    def zero(depth=0):
        """Return Zi(0, 0), or Zi(Zi(0, 0), Zi(0, 0)), or so on"""
        if isinstance(depth, int) and depth >= 0:
            if depth == 0:
                return Zi(0, 0)
            else:
                d = depth - 1
                return Zi(Zi.zero(d), Zi.zero(d))
        else:
            raise Exception(f"Cannot create a zero with {depth}")

    @staticmethod
    def one(depth=0):
        """Return Zi(1, 0), or Zi(Zi(1, 0), Zi(0, 0)), or so on"""
        if isinstance(depth, int) and depth >= 0:
            if depth == 0:
                return Zi(1, 0)
            else:
                d = depth - 1
                return Zi(Zi.one(d), Zi.zero(d))
        else:
            raise Exception(f"Cannot create a one with {depth}")

    # --------------------------

    def __pow__(self, n: int, modulo=None):
        """Implements the ** operator: self ** n.

        If n == 0, then Zi(1, 0) is returned. If n < 0, then the Gaussian
        rational, Qi, for 1 / self**n is returned. Otherwise, self ** n is returned.
        """
        result = self
        if isinstance(n, int):
            if n == 0:
                result = Zi(1)  # "1"
            elif n > 0:
                for _ in range(n - 1):
                    result = result * self
            else:  # n < 0
                result = 1 / (self ** abs(n))
        else:
            raise TypeError(f"The power, {n}, must be an integer.")
        return result

    def __eq__(self, other) -> bool:
        """Return True if this Zi equals other."""
        return (self.real == other.real) and (self.imag == other.imag)

    def __ne__(self, other) -> bool:
        """Return True if this Zi does NOT equal other."""
        return (self.real != other.real) or (self.imag != other.imag)

    def __hash__(self):
        """Allow this Zi to be hashed."""
        return hash((self.real, self.imag))

    def __abs__(self) -> float:
        """Returns the square root of the norm."""
        return sqrt(self.norm)

    def __pos__(self):
        return +self

    def __rpow__(self, base):
        return NotImplemented

    def __round__(self):
        if isinstance(self.real, Number) and isinstance(self.imag, Number):
            return Zi(round(self.real), round(self.imag))
        else:
            return self

    @staticmethod
    def eye():
        """Return i = Zi(0, 1)"""
        return Zi(0, 1)

    @staticmethod
    def units():
        """Returns the list of four units, [1, -1, i, -i], as Zis."""
        return [Zi(1), -Zi(1), Zi.eye(), -Zi.eye()]

    @property
    def is_unit(self):
        """Returns True if this Zi is a unit."""
        return self in Zi.units()

    @staticmethod
    def two():
        """Returns 1+i, because a Gaussian integer has an even norm if and only if
        it is a multiple of 1+i."""
        return Zi(1, 1)

    def associates(self):
        """Return a list of this Zi's three associates"""
        us = Zi.units()
        return list(map(lambda u: u * self, us[1:]))  # skip multiplying by 1

    # def is_associate(self, other):
    #     """Return True if the other Zi is an associate of this Zi
    #
    #     Otherwise, return False.
    #     """
    #     q = self // other
    #     if q:
    #         if q in Zi.units():
    #             return True
    #         else:
    #             return False
    #     else:
    #         return False

