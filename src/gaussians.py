"""Gaussian Integer & Rational Number Classes

A Gaussian integer is a complex number whose real and imaginary parts are both integers.
Similarly, a Gaussian rational is a complex number whose real and imaginary parts are
rational numbers.

In mathematics, Gaussian integers and rationals are denoted by Z[i] & Q[i], resp.
So, here, Zi & Qi denote the Gaussian integer and rational classes.

The classes support the arithmetic of Gaussian integers and rationals using the
operators: +, -, *, /, //, %, **, +=, -=, *=, and /=, along with a modified version
of divmod, modified_divmod, and two functions related to the Greatest Common Divisor:
gcd and xgcd.

Example:
  > from gaussians import Zi, Qi
  >
  > alpha = Zi(11, 3)
  > beta = Zi(1, 8)
  > a, x, y = Zi.xgcd(alpha, beta)
  > print(f"{alpha * x + beta * y} = {alpha} * {x} + {beta} * {y}")
  > (1-2j) = (11+3j) * (2-1j) + (1+8j) * 3j

"""

__author__ = "Alfred J. Reich, Ph.D."
__contact__ = "al.reich@gmail.com"
__copyright__ = "Copyright (C) 2024 Alfred J. Reich, Ph.D."
__license__ = "MIT"
__version__ = "1.0.0"

# from math import sqrt, floor, ceil
import math
from fractions import Fraction
from numbers import Complex
from random import randint
from functools import wraps
import numpy as np


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


class Zi(Complex):
    """Gaussian Integer Class with arithmetic and related functionality.

    A Gaussian integer, Zi, has two integer input values, re & im.
    Floats and complex numbers can be entered, but they will be rounded to the
    nearest integers. If a complex number is provided for re, then the value of
    im will be ignored, and the complex number's components, real & imag, will be
    rounded to nearest integers and used as inputs for re & im, respectively.
    """

    def __init__(self, re: (int, np.int64, float, complex) = 0, im: (int, float) = 0) -> None:
        """Instantiate a Gaussian integer, Zi(re=0, im=0)."""

        if isinstance(re, (int, np.int64)):
            self.__real = int(re)
        elif isinstance(re, float):
            self.__real = round(re)
        elif isinstance(re, complex):
            self.__real = round(re.real)
        else:
            raise TypeError(f"{re} cannot be used for the real part of a Zi instance")

        if isinstance(re, complex):  # This way, im is ignored if re is complex
            self.__imag = round(re.imag)
        elif isinstance(im, (int, np.int64)):
            self.__imag = int(im)
        elif isinstance(im, float):
            self.__imag = round(im)
        else:
            raise TypeError(f"{im} cannot be used for the imaginary part of a Zi instance")

    @property
    def real(self) -> int:
        return self.__real

    @property
    def imag(self) -> int:
        return self.__imag

    def __repr__(self) -> str:
        if self.imag == 0:
            return f"Zi({self.real})"
        else:
            return f"Zi({self.real}, {self.imag})"

    def __str__(self) -> str:
        if self.imag == 0:
            return str(self.real)
        else:
            return str(complex(self))

    # NOTE: Python ints and floats have both 'real' and 'imag' properties, so
    # no conversion to Gaussian integers is necessary to use them in the arithmetic
    # operations, below.

    def __add__(self, other):
        """Implements the + operator: self + other"""
        return Zi(self.real + other.real, self.imag + other.imag)

    def __radd__(self, other):
        """The reflected (swapped) operand for addition: other + self"""
        return Zi(other) + self

    def __iadd__(self, other):
        """Implements the += operation: self += other"""
        return Zi(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        """Implements the subtraction operator: self - other"""
        return Zi(self.real - other.real, self.imag - other.imag)

    def __rsub__(self, other):
        """The reflected (swapped) operand for subtraction: other - self"""
        return Zi(other) - self

    def __isub__(self, other):
        """Implements the -= operation: self -= other"""
        return Zi(self.real - other.real, self.imag - other.imag)

    # def __mul__(self, other):  # self * other
    #     """Implements the multiplication operator: self * other"""
    #     a = self.real
    #     b = self.imag
    #     c = round(other.real)
    #     d = round(other.imag)
    #     return Zi(a * c - b * d, a * d + b * c)

    def __mul__(self, other):  # self * other
        """Implements the multiplication operator: self * other"""
        if isinstance(other, Qi):
            return Qi(self) * other
        else:
            a = self.real
            b = self.imag
            c = round(other.real)
            d = round(other.imag)
            return Zi(a * c - b * d, a * d + b * c)

    def __rmul__(self, other):  # other * self
        """The reflected (swapped) operand for multiplication: other * self"""
        return Zi(other) * self

    def __imul__(self, other):
        """Implements the *= operation: self *= other"""
        a = self.real
        b = self.imag
        c = round(other.real)
        d = round(other.imag)
        return Zi(a * c - b * d, a * d + b * c)

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

    def __complex__(self) -> complex:
        """Return the complex number that corresponds to this Zi."""
        return complex(self.real, self.imag)

    def __neg__(self):
        """Negate this Zi."""
        return Zi(-self.real, -self.imag)

    def __eq__(self, other: Complex) -> bool:
        """Return True if this Zi equals other."""
        return (self.real == other.real) and (self.imag == other.imag)

    def __ne__(self, other) -> bool:
        """Return True if this Zi does NOT equal other."""
        return (self.real != other.real) or (self.imag != other.imag)

    @gaussian_rational
    def __truediv__(self, other):  # self / other
        """Divide self by other, exactly, and return the resulting Gaussian rational or integer.

        The divisor (other) is first cast into a Gaussian rational (Qi) prior to division.
        """
        return Qi(self) / other

    @gaussian_rational
    def __rtruediv__(self, other):  # other / self
        """Divide pother by self, exactly, and return the resulting Gaussian rational or integer.

        The dividend (other) is first cast into a Gaussian rational (Qi) prior to division.
        """
        return other / Qi(self)

    def __floordiv__(self, other):  # self // other
        """Implements the // operator using 'round', instead of 'floor'.

        Returns the closest integer approximation to the quotient, self / other,
        as a Zi, by rounding the real and imag parts after division, not flooring.
        'other' can be an int, float, complex, or Zi.
        """
        if isinstance(other, (int, float, complex, Zi)):
            return Zi(complex(self) / complex(other))
        else:
            raise TypeError(f"{other} is not a supported type.")

    def __rfloordiv__(self, other):  # other // self
        if isinstance(other, (int, float, complex)):
            return Zi(complex(other) / complex(self))
        else:
            raise TypeError(f"{other} is not a supported type.")

    def __mod__(self, other):
        """Implements the % operator.

        Returns the remainder of the result from modified_divmod
        """
        _, r = Zi.modified_divmod(self, other)
        return r

    def __hash__(self):
        """Allow this Zi to be hashed."""
        return hash((self.real, self.imag))

    def __abs__(self) -> float:
        """Returns the square root of the norm."""
        return math.sqrt(self.norm)

    def __pos__(self):
        return +self

    def __rpow__(self, base):
        return NotImplemented

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

    @property
    def conjugate(self):
        """Return the conjugate of this Gaussian integer"""
        return Zi(self.real, - self.imag)

    @property
    def norm(self) -> int:
        """Return the norm of this Gaussian integer.

        NOTE: The norm here is the square of the usual absolute value.
        """
        n = self * self.conjugate
        return n.real

    @staticmethod
    def random(re1=-100, re2=100, im1=-100, im2=100):
        """Return a random Gaussian integer with re1 <= re <= re2 and im1 <= im <= im2."""
        return Zi(randint(re1, re2), randint(im1, im2))

    def associates(self):
        """Return a list of this Zi's three associates"""
        us = Zi.units()
        return list(map(lambda u: u * self, us[1:]))  # skip multiplying by 1

    def is_associate(self, other):
        """Return True if the other Zi is an associate of this Zi

        Otherwise, return False.
        """
        q = self // other
        if q:
            if q in Zi.units():
                return True
            else:
                return False
        else:
            return False

    def to_gaussian_rational(self):
        """Convert this Gaussian integer to an equivalent Gaussian rational."""
        return Qi(self.real, self.imag)

    @staticmethod
    def norms_divide(a, b):
        """Divide the larger norm by the smaller norm. If they divide evenly,
        return the value; otherwise, if they don't divide evenly, return False."""
        x = a.norm
        y = b.norm
        sm = min(x, y)
        lg = max(x, y)
        if lg % sm == 0:
            return int(lg / sm)
        else:
            return False

    @staticmethod
    def from_array(arr):
        """Convert a two-element array into a Gaussian integer."""
        return Zi(int(arr[0]), int(arr[1]))

    # See https://kconrad.math.uconn.edu/blurbs/ugradnumthy/Zinotes.pdf
    @staticmethod
    def modified_divmod(a, b):
        """The divmod algorithm, modified for Gaussian integers.

        Returns q & r, such that a = b * q + r, where
        r.norm < b.norm / 2. This is the Modified Division
        Theorem described in 'The Gaussian Integers' by Keith Conrad
        """
        q = Zi(complex(a * b.conjugate) / b.norm)  # Zi rounds the complex result here
        r = a - b * q
        return q, r

    @staticmethod
    def gcd(a, b, verbose=False):
        """A gcd algorithm for Gaussian integers.
        Returns the greatest common divisor of a & b.

        This function implements the Euclidean algorithm for Gaussian integers.
        """
        zero = Zi()
        if a * b == zero:
            raise ValueError(f"Both inputs must be non-zero: {a} and {b}")
        else:
            r1, r2 = a, b
            while r2 != zero:
                r0, r1 = r1, r2
                q, r2 = Zi.modified_divmod(r0, r1)  # q only used in call to print, below
                if verbose:
                    print(f"   {r0} = {r1} * {q} + {r2}")
        return r1

    @staticmethod
    def xgcd(alpha, beta):
        """The Extended Euclidean Algorithm for Gaussian Integers.

        Three values are returned: gcd, x, & y, such that
        the Greatest Common Divisor (gcd) of alpha & beta can be
        written as gcd = alpha * x + beta * y. x & y are called
        Bézout's coefficients.
        """
        if isinstance(alpha, Zi) and isinstance(beta, Zi):
            zero = Zi()
        else:
            raise ValueError(f"Inputs must be two Zis.")

        # NOTE: Many of the lines below perform two assigment operations
        a, b = alpha, beta
        x, next_x = 1, 0
        y, next_y = 0, 1
        while b != zero:
            q = a // b
            next_x, x = x - q * next_x, next_x
            next_y, y = y - q * next_y, next_y
            a, b = b, a % b
        return a, x, y

    @staticmethod
    def congruent_modulo(a, b, c):
        """This method returns two values: The first value is True or False,
        depending on whether x is congruent to y modulo z;
        the second value is result of computing (a - b) / c."""
        w = (a - b) / c
        if isinstance(w, Zi):
            return True, w
        else:
            return False, w

    @staticmethod
    def is_relatively_prime(a, b) -> bool:
        """Returns True if a and b are relatively prime, otherwise it returns false."""
        return Zi.gcd(a, b) in Zi.units()

    # Defining "is_gaussian_prime" as a staticmethod allows it to be easily used on both
    # Gaussian integers and real integers. If it had been defined as a normal method,
    # then it wouldn't work on real integers, unless they are first converted into Zi's.
    @staticmethod
    def is_gaussian_prime(x) -> bool:
        """Return True if x is a Gaussian prime.  Otherwise, return False.
        x can be an integer or a Gaussian integer.

        See https://mathworld.wolfram.com/GaussianPrime.html
        """
        re = im = norm = None  # So PyCharm won't complain about using variables before assigning them

        if isinstance(x, Zi):
            re = abs(x.real)
            im = abs(x.imag)
            norm = x.norm
        elif isinstance(x, int):
            re = abs(x)
            im = 0
            norm = re * re

        if (re * im != 0) and isprime(norm):
            return True

        elif re == 0:
            if isprime(im) and (im % 4 == 3):
                return True
            else:
                return False

        elif im == 0:
            if isprime(re) and (re % 4 == 3):
                return True
            else:
                return False

        else:
            return False

def isprime(n: int) -> bool:
    """Returns True if n is a positive, prime integer; otherwise, False is returned.

    NOTE: A more efficient version of this function, by the same name, exists in SymPy.
    """
    if isinstance(n, int):
        if n == 2:
            return True
        if n % 2 == 0 or n <= 1:
            return False
        root_n = int(math.sqrt(n)) + 1
        for val in range(3, root_n, 2):
            if n % val == 0:
                return False
        return True
    else:
        raise False

class Qi(Complex):
    """Gaussian Rational Number Class"""

    __max_denominator = 1_000_000

    def __init__(self, re: (str, int, float, complex, Zi, Fraction) = Fraction(0, 1),
                 im: (str, int, float, Fraction) = Fraction(0, 1)):

        if isinstance(re, Fraction):
            self.__real = re
        elif isinstance(re, (str, int, float)):
            self.__real = Fraction(re).limit_denominator(self.__max_denominator)
        elif isinstance(re, (complex, Zi)):
            self.__real = Fraction(re.real).limit_denominator(self.__max_denominator)
        else:
            raise TypeError(f"{re} is not a supported type")

        if isinstance(re, (complex, Zi)):
            self.__imag = Fraction(re.imag).limit_denominator(self.__max_denominator)
        elif isinstance(im, Fraction):
            self.__imag = im
        elif isinstance(im, (str, int, float)):
            self.__imag = Fraction(im).limit_denominator(self.__max_denominator)
        else:
            raise TypeError(f"{im} is not a supported type")

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
        return self.__real

    @property
    def imag(self) -> Fraction:
        return self.__imag

    def __repr__(self):
        return f"Qi({repr(str(self.real))}, {repr(str(self.imag))})"

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
        else:
            raise TypeError(f"The power, {n}, must be an integer.")
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

    @gaussian_rational
    def __eq__(self, other: Complex) -> bool:
        """Test for equality."""
        return (self.real == other.real) and (self.imag == other.imag)

    @gaussian_rational
    def __ne__(self, other) -> bool:
        """Return True if this Qi does NOT equal other."""
        return (self.real != other.real) or (self.imag != other.imag)

    def __hash__(self):
        return hash((self.real, self.imag))

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

    @staticmethod
    def random(re1=-100, re2=100, im1=-100, im2=100):
        """Return a random Gaussian rational"""
        if re1 < re2 and im1 < im2 and re2 >= 1 and im2 >= 1:
            numerator = Zi.random(re1, re2, im1, im2)
            denominator = Zi.random(1, re2, 1, im2)
        else:
            raise ValueError(f"Bad range")
        return numerator / denominator

    @property
    def inverse(self):
        conj = self.conjugate
        norm = self.norm
        return Qi(conj.real / norm, conj.imag / norm)

    @staticmethod
    def eye():
        """Return i = Qi(0, 1)"""
        return Qi(0, 1)

    @staticmethod
    def units():
        """Returns the list of four units, [1, -1, i, -i], as Qis."""
        return [Qi(1), -Qi(1), Qi.eye(), -Qi.eye()]

    def associates(self):
        """Return a list of this Qi's three associates"""
        us = Qi.units()
        return list(map(lambda u: u * self, us[1:]))  # skip multiplying by 1

    def is_associate(self, other):
        """Return True if the other Qi is an associate of this Qi, return False otherwise"""
        q = self / other
        if q:
            if q in Zi.units():
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def string_to_rational(qi_str):
        """Turn the string form of a Gaussian rational into a Gaussian rational."""

        insides = qi_str[1:-2]  # Remove leading ( and trailing j)

        # Separate leading sign, if exists, from main body of string
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
