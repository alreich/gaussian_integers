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
    """Integer-valued quaternions ('Gaussian quaternions')"""

    def __init__(self,
                 a: (int, np.int64) = 1,
                 b: (int, np.int64) = 0,
                 c: (int, np.int64) = 0,
                 d: (int, np.int64) = 0):
        if isinstance(a, (int, np.int64)):
            self.__arr = np.array([a, b, c, d], dtype=np.int64)
        elif isinstance(a, np.ndarray):
            self.__arr = a

    @property
    def real(self) -> int:
        return int(self.__arr[0])

    @property
    def imag(self):
        return tuple(self.__arr[1:])

    @property
    def array(self):
        return self.__arr

    @property
    def conjugate(self):
        a, b, c, d = self.array
        return Hi(a, -b, -c, -d)

    @property
    def norm(self) -> int:
        tmp = self * self.conjugate
        return int(tmp.real)

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
        return self.array == other.array

    def __ne__(self, other):
        return self.array != other.array

    def __mul__(self, other):
        a1, b1, c1, d1 = self.array
        a2, b2, c2, d2 = other.array
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
    def mul_as_gaussian_ints(q1, q2):
        """Implements quaternion multiplication by first converting each one into
        two Gaussian integers, Zi, and then multiplying the Zi according to the
        Cayley-Dickson construction
        """
        a, b = q1.to_gaussian_ints()
        c, d = q2.to_gaussian_ints()
        # (a, b) * (c, d) = (a * c - d.conj * b, d * a + b * c.conj)
        z1 = a * c - d.conjugate * b
        z2 = d * a + b * c.conjugate
        return Hi(z1.real, z1.imag, z2.real, z2.imag)

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


def split_array(arr):
    n = len(arr) // 2
    return arr[:n], arr[n:]
