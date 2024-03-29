"""Integer-Valued Quaternions"""

__author__ = "Alfred J. Reich, Ph.D."
__contact__ = "al.reich@gmail.com"
__copyright__ = "Copyright (C) 2024 Alfred J. Reich, Ph.D."
__license__ = "MIT"
__version__ = "1.0.0"

import numpy as np
import random as rnd
import math
from gaussians import Zi


class Hi:
    """Integer-valued quaternions ('Gaussian quaternions')

    Internally, a quaternion integer is implemented as a numpy array of 4
    integers, but they can be thought of as simply 4 integers, or 2 Gaussian
    integers. For this reason, a Hi can be constructed from 4 integers, or
    2 Gaussian integers, or 1 numpy array of 4 integers.
    """
    def __init__(self,
                 # If no inputs are given, then the "zero" quaternion will be returned
                 z1: (Zi, np.ndarray, int) = Zi(),
                 z2: (Zi, int) = Zi(),
                 z3: int = 0,
                 z4: int = 0):

        # Assumes two Gaussian integers provided, z1 & z2
        if isinstance(z1, Zi):
            self.__arr = np.array([z1.real, z1.imag, z2.real, z2.imag], dtype=np.int64)

        # Assumes one numpy array containing four np.int64's provided, z1
        elif isinstance(z1, np.ndarray):
            self.__arr = z1

        # Assumes four ints or np.int64s provided, z1, ..., z4
        elif isinstance(z1, (int, np.int64)):
            self.__arr = np.array([z1, z2, z3, z4], dtype=np.int64)
        else:
            raise ValueError(f"{type(z1)} not supported")

    @property
    def gaussian_ints(self):
        arr = self.__arr
        n = len(arr) // 2
        return Zi.from_array(arr[:n]), Zi.from_array(arr[n:])

    @property
    def real(self):
        real, _ = self.gaussian_ints
        return real

    @property
    def imag(self):
        _, imag = self.gaussian_ints
        return imag

    @property
    def array(self):
        return self.__arr

    @property
    def conjugate(self):
        real, imag = self.gaussian_ints
        return Hi(real.conjugate, -imag)

    @property
    def norm(self) -> int:
        tmp = self * self.conjugate
        return int(tmp.array[0])

    def show(self):
        real, imag = self.gaussian_ints
        return f"Hi({repr(real)}, {repr(imag)})"

    def __abs__(self) -> float:
        return math.sqrt(self.norm)

    def __repr__(self) -> str:
        a, b, c, d = self.array
        return f"Hi({a}, {b}, {c}, {d})"

    def __str__(self) -> str:
        a, b, c, d = self.array
        return f"({a} + {b}i + {c}j + {d}k)"

    def __add__(self, other):
        return Hi(self.array + other.array)

    def __sub__(self, other):
        return Hi(self.array - other.array)

    def __neg__(self):
        return Hi(-self.array)

    def __eq__(self, other):
        return np.array_equal(self.array, other.array)

    def __ne__(self, other):
        return not self == other

    def __mul__(self, other):
        """Multiplication according to the Cayley-Dickson construction"""
        a, b = self.gaussian_ints
        c, d = other.gaussian_ints
        # (a, b) * (c, d) = (a * c - d.conj * b, d * a + b * c.conj)
        z1 = a * c - d.conjugate * b
        z2 = d * a + b * c.conjugate
        return Hi(z1, z2)

    @staticmethod
    def hamilton_product(q1, q2):
        """Multiplication according to the classic Hamilton product"""
        a1, b1, c1, d1 = q1.array
        a2, b2, c2, d2 = q2.array
        # See https://en.wikipedia.org/wiki/Quaternion#Hamilton_product
        a = a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2
        b = a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2
        c = a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2
        d = a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2
        return Hi(a, b, c, d)

    def scalar_mul(self, scalar):
        """Multiply this quaternion by a scalar integer.

        Round the scalar to the nearest integer if necessary.
        """
        return Hi(round(scalar) * self.array)

    def __floordiv__(self, other):
        """Implements the // operator using 'round', instead of 'floor'."""
        numer = self * other.conjugate
        denom = other.norm
        quotient = np.round(numer.array / denom)
        return Hi(quotient.astype(np.int64))

    def to_gaussian_ints(self):
        """Convert this quaternion into two Gaussian integers"""
        a, b, c, d = self.array
        return Zi(int(a), int(b)), Zi(int(c), int(d))

    @staticmethod
    def random(low=-100, high=100):
        return Hi(np.array([rnd.randint(low, high) for _ in range(4)]))

    @staticmethod
    def modified_divmod(a, b):
        """Returns q & r, such that a = b * q + r, where
        r.norm < b.norm / 2
        """
        q = a // b
        r = a - b * q
        return q, r

    @staticmethod
    def from_string(s):
        """Converts the string form of a Hi back into a Hi.

        Example:
        Hi.from_string('(46 + -92i + 9j + 23k)') -> Hi(46, -92, 9, 23)
        """
        return Hi(np.array(list(map(lambda x: int(x),
                                    s.translate({ord(i): None for i in 'ijk'}
                                                )[1:-1].split(' + ')))))
