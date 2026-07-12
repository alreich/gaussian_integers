# Gaussian Integers Modulo n

__author__ = "Alfred J. Reich, Ph.D."
__contact__ = "al.reich@gmail.com"
__copyright__ = "Copyright (C) 2024 Alfred J. Reich, Ph.D."
__license__ = "MIT"
__version__ = "0.0.1"

import math
from numbers import Complex
from random import randint


class Zni:
    """Gaussian Integer Class with arithmetic and related functionality.

    A Gaussian integer, Zni, has two integer input values, re & im.
    Floats and complex numbers can be entered, but they will be rounded to the
    nearest integers. If a complex number is provided for re, then the value of
    im will be ignored. Additionally, the complex number's components, real & imag,
    will be rounded to the nearest integers and used as inputs for re & im, resp.
    """

    __n = 7

    def __init__(self, re=None, im=None):
        if isinstance(re, (float, int)):
            self.__re = round(re) % Zni.__n
            if im is None:
                self.__im = 0
            elif isinstance(im, (float, int)):
                self.__im = round(im) % Zni.__n
            else:
                raise Exception(f"Inputs incompatible: {re} and {im}")
        elif isinstance(re, complex):
            if im is None:
                self.__re = round(re.real) % Zni.__n
                self.__im = round(re.imag) % Zni.__n
            elif isinstance(im, (complex, Zni)):
                self.__re = Zni(re) % Zni.__n
                self.__im = Zni(im) % Zni.__n
            else:
                raise Exception(f"Inputs incompatible: {re} and {im}")
        elif isinstance(re, Zni):
            if im is None:
                self.__re = re.real % Zni.__n
                self.__im = re.imag % Zni.__n
            elif isinstance(im, (complex, Zni)):
                self.__re = Zni(re) % Zni.__n
                self.__im = Zni(im) % Zni.__n
            else:
                raise Exception(f"Inputs incompatible: {re} and {im}")
        elif re is None:
            if im is None:
                self.__re = 0
                self.__im = 0
            else:
                raise Exception("If re is None, then im must be None. But im = {im}")
        else:
            raise Exception("We should never get to this point in the code")

    @staticmethod
    def modulo_value():
        return Zni.__n

    @staticmethod
    def set_modulo_value(value):
        Zni.__n = value
        return Zni.__n

    @property
    def real(self):
        return self.__re

    @property
    def imag(self):
        return self.__im

    def __repr__(self) -> str:
        if self.imag == 0:
            return f"Zni({self.real})"
        else:
            return f"Zni({self.real}, {self.imag})"

    def __str__(self) -> str:
        if self.imag == 0:
            return str(self.real)
        else:
            return str(complex(self))

    def __getitem__(self, index):
        return self.to_array()[index]

    # NOTE: Python ints and floats have both 'real' and 'imag' properties, so
    # no conversion to Gaussian integers is necessary to use them in the arithmetic
    # operations, below.

    def __add__(self, other):
        """Implements the + operator: self + other"""
        return Zni((self.real + other.real) % Zni.__n, (self.imag + other.imag) % Zni.__n)

    def __radd__(self, other):
        """The reflected (swapped) operand for addition: other + self"""
        return Zni(other) + self

    def __iadd__(self, other):
        """Implements the += operation: self += other"""
        return Zni((self.real + other.real) % Zni.__n, (self.imag + other.imag) % Zni.__n)

    def __sub__(self, other):
        """Implements the subtraction operator: self - other"""
        return Zni((self.real - other.real) % Zni.__n, (self.imag - other.imag) % Zni.__n)

    def __rsub__(self, other):
        """The reflected (swapped) operand for subtraction: other - self"""
        return Zni(other) - self

    def __isub__(self, other):
        """Implements the -= operation: self -= other"""
        return Zni((self.real - other.real) % Zni.__n, (self.imag - other.imag) % Zni.__n)

    def __mul__(self, other):  # self * other
        """Implements the multiplication operator: self * other"""
        a = self.real
        b = self.imag
        c = round(other.real)
        d = round(other.imag)
        return Zni((a * c - b * d) % Zni.__n, (a * d + b * c) % Zni.__n)

    def __rmul__(self, other):  # other * self
        """The reflected (swapped) operand for multiplication: other * self"""
        return Zni(other) * self

    def __imul__(self, other):
        """Implements the *= operation: self *= other"""
        a = self.real
        b = self.imag
        c = round(other.real)
        d = round(other.imag)
        return Zni((a * c - b * d) % Zni.__n, (a * d + b * c) % Zni.__n)

    def __pow__(self, n: int, modulo=None):
        """Implements the ** operator: self ** n.

        If n == 0, then Zni(1, 0) is returned. If n < 0, then the Gaussian
        rational, Qi, for 1 / self**n is returned. Otherwise, self ** n is returned.
        """
        result = self
        if isinstance(n, int):
            if n == 0:
                result = Zni(1)  # "1"
            elif n > 0:
                for _ in range(n - 1):
                    result = result * self
            else:
                raise Exception("The power must be a non-negative integer")
        else:
            raise Exception("The power must be an integer")
        return result

    def __complex__(self) -> complex:
        """Return the complex number that corresponds to this Zni."""
        return complex(self.real, self.imag)

    def __neg__(self):
        """Negate this Zni."""
        return Zni(-self.real, -self.imag)

    def __eq__(self, other: Complex) -> bool:
        """Return True if this Zni equals other."""
        return (self.real == other.real) and (self.imag == other.imag)

    def __ne__(self, other) -> bool:
        """Return True if this Zni does NOT equal other."""
        return (self.real != other.real) or (self.imag != other.imag)

    def __floordiv__(self, other):  # self // other
        """Implements the // operator using 'round', instead of 'floor'.

        Returns the closest integer approximation to the quotient, self / other,
        as a Zni, by rounding the real and imag parts after division, not flooring.
        'other' can be an int, float, complex, or Zni.
        """
        if isinstance(other, (int, float, complex, Zni)):
            return Zni(complex(self) / complex(other))
        else:
            raise TypeError(f"{other} is not a supported type.")

    def __rfloordiv__(self, other):  # other // self
        if isinstance(other, (int, float, complex)):
            return Zni(complex(other) / complex(self))
        else:
            raise TypeError(f"{other} is not a supported type.")

    # def __mod__(self, other):
    #     """Implements the % operator.
    #
    #     Returns the remainder of the result from modified_divmod
    #     """
    #     if isinstance(other, (int, float, complex)):
    #         oth = Zni(other)
    #     else:
    #         oth = other
    #     _, r = Zni.modified_divmod(self, oth)
    #     return r

    def __hash__(self):
        """Allow this Zni to be hashed."""
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
        """Return i = Zni(0, 1)"""
        return Zni(0, 1)

    @staticmethod
    def units():
        """Returns the list of four units, [1, -1, i, -i], as Znis."""
        return [Zni(1), -Zni(1), Zni.eye(), -Zni.eye()]

    @property
    def is_unit(self):
        """Returns True if this Zni is a unit."""
        return self in Zni.units()

    @staticmethod
    def two():
        """Returns 1+i, because a Gaussian integer has an even norm if and only if
        it is a multiple of 1+i."""
        return Zni(1, 1)

    @property
    def conjugate(self):
        """Return the conjugate of this Gaussian integer"""
        return Zni(self.real, - self.imag)

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
        return Zni(randint(re1, re2), randint(im1, im2))

    def associates(self):
        """Return a list of this Zni's three associates"""
        us = Zni.units()
        return list(map(lambda u: u * self, us[1:]))  # skip multiplying by 1

    def is_associate(self, other):
        """Return True if the other Zni is an associate of this Zni

        Otherwise, return False.
        """
        q = self // other
        if q:
            if q in Zni.units():
                return True
            else:
                return False
        else:
            return False

    def to_array(self):
        """Convert this Gaussian integer to a two-integer array."""
        return self.real, self.imag

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
        return Zni(int(arr[0]), int(arr[1]))

    # See https://kconrad.math.uconn.edu/blurbs/ugradnumthy/Zinotes.pdf
    @staticmethod
    def modified_divmod(a, b):
        """The divmod algorithm, modified for Gaussian integers.

        Returns q & r, such that a = b * q + r, where
        r.norm < b.norm / 2. This is the Modified Division
        Theorem described in 'The Gaussian Integers' by Keith Conrad
        """
        q = Zni(complex(a * b.conjugate) / b.norm)  # Zni rounds the complex result here
        r = a - b * q
        return q, r

    @staticmethod
    def gcd(a, b, verbose=False):
        """A gcd algorithm for Gaussian integers.
        Returns the greatest common divisor of a & b.

        This function implements the Euclidean algorithm for Gaussian integers.
        """
        zero = Zni()
        if a * b == zero:
            raise ValueError(f"Both inputs must be non-zero: {a} and {b}")
        else:
            r1, r2 = a, b
            while r2 != zero:
                r0, r1 = r1, r2
                q, r2 = Zni.modified_divmod(r0, r1)  # q only used in call to print, below
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
        if isinstance(alpha, Zni) and isinstance(beta, Zni):
            zero = Zni()
        else:
            raise ValueError(f"Inputs must be two Znis.")

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
        the second value is the result of computing (a - b) / c."""
        w = (a - b) / c
        if isinstance(w, Zni):
            return True, w
        else:
            return False, w

    @staticmethod
    def is_relatively_prime(a, b) -> bool:
        """Returns True if a and b are relatively prime, otherwise it returns false."""
        return Zni.gcd(a, b) in Zni.units()

    # Defining "is_gaussian_prime" as a staticmethod allows it to be easily used on both
    # Gaussian integers and real integers. If it had been defined as a normal method,
    # then it wouldn't work on real integers unless they are first converted into Zi's.
    # @staticmethod
    # def is_gaussian_prime(x) -> bool:
    #     """Return True if x is a Gaussian prime.  Otherwise, return False.
    #     x can be an integer or a Gaussian integer.
    #
    #     See https://mathworld.wolfram.com/GaussianPrime.html
    #     """
    #     re = im = norm = None  # So PyCharm won't complain about using variables before assigning them
    #
    #     if isinstance(x, Zi):
    #         re = abs(x.real)
    #         im = abs(x.imag)
    #         norm = x.norm
    #     elif isinstance(x, int):
    #         re = abs(x)
    #         im = 0
    #         norm = re * re
    #
    #     if (re * im != 0) and isprime(norm):
    #         return True
    #
    #     elif re == 0:
    #         if isprime(im) and (im % 4 == 3):
    #             return True
    #         else:
    #             return False
    #
    #     elif im == 0:
    #         if isprime(re) and (re % 4 == 3):
    #             return True
    #         else:
    #             return False
    #
    #     else:
    #         return False

# def isprime(n: int) -> bool:
#     """Returns True if n is a positive, prime integer; otherwise, False is returned.
#
#     NOTE: A more efficient version of this function, by the same name, exists in SymPy.
#     """
#     if isinstance(n, int):
#         if n == 2:
#             return True
#         if n % 2 == 0 or n <= 1:
#             return False
#         root_n = int(math.sqrt(n)) + 1
#         for val in range(3, root_n, 2):
#             if n % val == 0:
#                 return False
#         return True
