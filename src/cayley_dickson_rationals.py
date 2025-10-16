# Cayley-Dickson Algebra with rational components

from fractions import Fraction
from functools import wraps
import math

from cayley_dickson_base import CayleyDicksonBase
from cayley_dickson_integers import Zi

def to_gaussian_rational(number):
    """Given a number, return its equivalent Gaussian rational."""
    if isinstance(number, (int, float, complex, Zi, Fraction)):
        return Qi(number)
    elif isinstance(number, Qi):
        return number
    else:
        raise TypeError(f"'{number}' cannot be cast into a Gaussian rational")

def gaussian_rational(fnc):
    """For use as a property that casts an argument into Gaussian rational."""
    @wraps(fnc)
    def gaussian_rational_wrapper(arg, num):
        qi = to_gaussian_rational(num)
        return fnc(arg, qi)
    return gaussian_rational_wrapper

class Qi(CayleyDicksonBase):
    """Cayley-Dickson Algebra with rational components"""

    __max_denominator = 1_000_000

    def __init__(self, real=Fraction(0, 1), imag=Fraction(0, 1)):

        if isinstance(real, Fraction):
            self.__re = real
        elif isinstance(real, (str, int, float)):
            self.__re = Fraction(real).limit_denominator(self.__max_denominator)
        elif isinstance(real, (complex, Zi)):
            self.__re = Fraction(real.real).limit_denominator(self.__max_denominator)
        else:
            raise TypeError(f"{real} is not a supported type")

        if isinstance(real, (complex, Zi)):
            self.__im = Fraction(real.imag).limit_denominator(self.__max_denominator)
        elif isinstance(imag, Fraction):
            self.__im = imag
        elif isinstance(imag, (str, int, float)):
            self.__im = Fraction(imag).limit_denominator(self.__max_denominator)
        else:
            raise TypeError(f"{imag} is not a supported type")

    @classmethod
    def max_denominator(cls):
        return cls.__max_denominator

    @classmethod
    def set_max_denominator(cls, value):
        if value > 1:
            cls.__max_denominator = value
            return cls.__max_denominator
        else:
            raise ValueError("max_denominator must be > 1")

    @property
    def real(self) -> Fraction:
        return self.__re

    @property
    def imag(self) -> Fraction:
        return self.__im

    # def __repr__(self):
    #     return f"Qi({repr(str(self.real))}, {repr(str(self.imag))})"

    def __str__(self):
        if self.imag < 0:
            return f"({self.real}{self.imag}j)"
        else:
            return f"({self.real}+{self.imag}j)"

    @gaussian_rational
    def __add__(self, other):
        return Qi(self.real + other.real, self.imag + other.imag)

    @gaussian_rational
    def __radd__(self, other):
        return other + self

    @gaussian_rational
    def __sub__(self, other):
        return Qi(self.real - other.real, self.imag - other.imag)

    @gaussian_rational
    def __rsub__(self, other):
        return other - self

    @gaussian_rational
    def __mul__(self, other):
        a = self.real
        b = self.imag
        c = other.real
        d = other.imag
        re = a * c - b * d
        im = a * d + b * c
        # Return a Gaussian integer if the denominators are 1
        if re.denominator == 1 and im.denominator == 1:
            return Zi(re.numerator, im.numerator)
        else:
            return Qi(re, im)

    @gaussian_rational
    def __rmul__(self, other):
        return other * self

    def __pow__(self, n: int, modulo=None):  # self ** n
        result = self
        if isinstance(n, int):
            if n == 0:
                result = Qi(Fraction(1, 1), Fraction(0, 1))  # "1"
            elif n > 0:
                for _ in range(n - 1):
                    result = result * self
            else:  # n < 0
                result = 1 / self ** abs(n)
        # else:
        #     raise TypeError(f"The power, {n}, must be an integer.")
        return result

    @gaussian_rational
    def __truediv__(self, other):
        """Returns self/other as a Gaussian rational"""
        return self * other.inverse

    @gaussian_rational
    def __rtruediv__(self, other):
        """Returns other/self as a Gaussian rational, Qi"""
        return other * self.inverse

    def __neg__(self):
        return Qi(-self.real, -self.imag)

    def __complex__(self) -> complex:
        return complex(float(self.real), float(self.imag))

    # @gaussian_rational
    # def __eq__(self, other: Complex) -> bool:
    #     """Test for equality."""
    #     return (self.real == other.real) and (self.imag == other.imag)
    #
    # @gaussian_rational
    # def __ne__(self, other) -> bool:
    #     """Return True if this Qi does NOT equal other."""
    #     return (self.real != other.real) or (self.imag != other.imag)
    #
    # def __hash__(self):
    #     return hash((self.real, self.imag))

    def __abs__(self) -> float:
        return math.sqrt(self.norm)

    def __pos__(self):
        return +self

    def __rpow__(self, **kwargs):
        return NotImplemented

    def __round__(self) -> Zi:
        return Zi(round(self.real), round(self.imag))

    def __floor__(self) -> Zi:
        return Zi(math.floor(self.real), math.floor(self.imag))

    def __ceil__(self) -> Zi:
        return Zi(math.ceil(self.real), math.ceil(self.imag))

    @property
    def conjugate(self):
        return Qi(self.real, -self.imag)

    @property
    def norm(self) -> Fraction:
        tmp = self * self.conjugate
        return tmp.real

    # @staticmethod
    # def random(re1=-100, re2=100, im1=-100, im2=100):
    #     """Return a random Gaussian rational"""
    #     if re1 < re2 and im1 < im2 and re2 >= 1 and im2 >= 1:
    #         numerator = Zi.random(re1, re2, im1, im2)
    #         denominator = Zi.random(1, re2, 1, im2)
    #     else:
    #         raise ValueError(f"Bad range")
    #     return numerator / denominator

    @property
    def inverse(self):
        conj = self.conjugate
        norm = self.norm
        return Qi(conj.real / norm, conj.imag / norm)

    # @staticmethod
    # def eye():
    #     """Return i = Qi(0, 1)"""
    #     return Qi(0, 1)
    #
    # @staticmethod
    # def units():
    #     """Returns the list of four units, [1, -1, i, -i], as Qis."""
    #     return [Qi(1), -Qi(1), Qi.eye(), -Qi.eye()]
    #
    # def associates(self):
    #     """Return a list of this Qi's three associates"""
    #     us = Qi.units()
    #     return list(map(lambda u: u * self, us[1:]))  # skip multiplying by 1
    #
    # def is_associate(self, other):
    #     """Return True if the other Qi is an associate of this Qi, return False otherwise"""
    #     q = self / other
    #     if q:
    #         if q in Zi.units():
    #             return True
    #         else:
    #             return False
    #     else:
    #         return False

    @staticmethod
    def string_to_rational(qi_str):
        """Turn the string form of a Gaussian rational into a Gaussian rational."""

        insides = qi_str[1:-2]  # Remove leading (and trailing j)

        # Separate leading sign, if it exists, from the main body of the string
        if insides[0] == '-' or insides[0] == '+':
            sign = insides[0]  # Leading sign
            body = insides[1:]
        else:
            sign = ''  # No leading sign
            body = insides

        # Split body of string into real & imag parts, based on imag sign
        if '+' in body:
            re, im = body.split('+')
            return Qi(sign + re, im)
        elif '-' in body:
            re, im = body.split('-')
            return Qi(sign + re, '-' + im)
        else:
            raise ValueError(f"Can't parse {qi_str}")