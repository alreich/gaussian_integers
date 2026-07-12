"""Gaussian integer (Zi) class: a + bi with a, b in Z."""

from math import sqrt
from numbers import Complex
import random as rnd


class Zi(Complex):
    """A class that represents a Gaussian integer. In mathematics, the set of all integers
    is denoted by Z, and the set of all Gaussian integers is denoted by Z[i]."""

    __slots__ = ('_real', '_imag')

    def __init__(self, real = None, imag = None) -> None:
        if isinstance(real, (complex, Zi)):
            if imag is None:
                super().__setattr__('_real', round(real.real))
                super().__setattr__('_imag', round(real.imag))
            else:
                raise TypeError(f"imag must be None if real is a complex: {imag}")
        elif isinstance(real, (int, float)):
            super().__setattr__('_real', round(real))
            if isinstance(imag, (int, float)):
                super().__setattr__('_imag', round(imag))
            elif imag is None:
                super().__setattr__('_imag', 0)
            else:
                raise TypeError(f"Invalid type for imag: {imag}")
        elif real is None and imag is None:
            super().__setattr__('_real', 0)
            super().__setattr__('_imag', 0)
        else:
            raise TypeError(f"Invalid type for real: {real}")

    # ---------------- Accessors -----------------------

    @property
    def real(self) -> int:
        return self._real

    @property
    def imag(self) -> int:
        return self._imag

    def __getitem__(self, idx):
        if idx == 0:
            return self.real
        elif idx == 1:
            return self.imag
        raise IndexError("Zi index out of range (must be 0 or 1)")

    # ---------------- Type Cast -----------------------

    @staticmethod
    def _ensure_zi(x):
        if isinstance(x, Zi):
            return x
        if isinstance(x, complex):
            return Zi(x)
        if isinstance(x, (int, float)):
            return Zi(x, 0)
        raise TypeError(f"Cannot convert {type(x)} to Zi")

    # ---------------- Equality -----------------------

    def __eq__(self, other):
        """If other can be cast to a Zi, and if self is equal to that,
        then self == other."""
        try:
            oth = Zi._ensure_zi(other)
        except TypeError:
            return NotImplemented
        return self.real == oth.real and self.imag == oth.imag

    def __ne__(self, other):
        """Inverse of __eq__. Must correctly propagate NotImplemented so that
        Python falls back to the other operand's __eq__/__ne__ instead of
        treating an incomparable type as simply 'not equal'."""
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    # ---------------- Univariate Methods -----------------------

    def __repr__(self):
        return f"Zi({self.real}, {self.imag})"

    def __str__(self):
        if self.imag == 0:
            return str(self._real)
        return str(complex(self.real, self.imag))

    def __hash__(self):
        return hash((self.real, self.imag))

    def __complex__(self):
        return complex(self.real, self.imag)

    def __abs__(self):
        return sqrt(self.norm())

    def __neg__(self):
        return Zi(-self._real, -self.imag)

    def __pos__(self):
        return Zi(self._real, self.imag)

    def __bool__(self):
        """True if at least one component (real or imag) is non-zero"""
        return self.real != 0 or self.imag != 0

    def conjugate(self):
        return Zi(self._real, -self.imag)

    def norm(self):
        return self.real * self.real + self.imag * self.imag

    # ---------------- Arithmetic -----------------------------

    def __add__(self, other):
        oth = Zi._ensure_zi(other)
        return Zi(self.real + oth.real, self.imag + oth.imag)

    def __radd__(self, other):
        oth = Zi._ensure_zi(other)
        return oth + self

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        oth = Zi._ensure_zi(other)
        return Zi(self.real - oth.real, self.imag - oth.imag)

    def __rsub__(self, other):
        oth = Zi._ensure_zi(other)
        return oth - self

    def __isub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        oth = Zi._ensure_zi(other)
        a, b = self
        c, d = oth
        return Zi(a * c - b * d, a * d + b * c)

    def __rmul__(self, other):
        oth = Zi._ensure_zi(other)
        return oth * self

    def __imul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        """Division rounded to the nearest Gaussian integer. Uses exact
        integer arithmetic (multiply by conjugate, divide by norm) rather
        than floating-point complex division, so it stays precise for
        arbitrarily large coefficients."""
        oth = Zi._ensure_zi(other)
        n = oth.norm()
        if n == 0:
            raise ZeroDivisionError("division by zero Gaussian integer")
        num = self * oth.conjugate()
        return Zi(round(num.real / n), round(num.imag / n))  # type: ignore

    def __rtruediv__(self, other):
        oth = Zi._ensure_zi(other)
        return oth.__truediv__(self)

    def __floordiv__(self, other):
        """Gaussian integers have no natural total order, so 'floor'
        division is defined the same way as __truediv__: round to the
        nearest Gaussian integer. Delegates to __truediv__ so both operators
        agree exactly (previously this used float-based complex division,
        which could disagree with __truediv__'s exact result on large
        coefficients due to floating-point rounding)."""
        return self.__truediv__(other)

    def __rfloordiv__(self, other):
        other_zi = Zi._ensure_zi(other)
        return other_zi.__floordiv__(self)

    def __mod__(self, other):
        other_zi = Zi._ensure_zi(other)
        q = self // other_zi
        return self - other_zi * q

    def __pow__(self, exponent):
        if not isinstance(exponent, int):
            return NotImplemented
        if exponent == 0:
            return Zi(1, 0)
        base, exp = (self, exponent) if exponent > 0 else (Zi(1, 0) / self, -exponent)
        result = Zi(1, 0)
        while exp > 0:
            if exp & 1:
                result = result * base
            base = base * base
            exp >>= 1
        return result

    def __rpow__(self, base):
        if self.imag != 0:
            return NotImplemented
        return Zi._ensure_zi(base).__pow__(self.real)

    # ---------- Array Conversion ----------

    def to_array(self):
        return [self.real, self.imag]

    @staticmethod
    def from_array(arr):
        if len(arr) != 2:
            raise ValueError("Array must have exactly two elements")
        return Zi(arr[0], arr[1])

    # ---------- Prime Numbers ----------

    @staticmethod
    def _is_rational_prime(n):
        """True if the plain (rational) integer n is prime. This is a
        helper for is_gaussian_prime, not a statement about Gaussian
        primality."""
        n = abs(int(n))
        if n < 2:
            return False
        if n in (2, 3):
            return True
        if n % 2 == 0:
            return False
        i = 3
        while i * i <= n:
            if n % i == 0:
                return False
            i += 2
        return True

    @staticmethod
    def is_gaussian_prime(x):
        """A Gaussian integer a+bi is prime iff:
        - both a,b are nonzero and a^2+b^2 is a rational prime, or
        - one of a,b is zero and the other has absolute value c, where c is
          a rational prime with c % 4 == 3 (primes p == 2 or p == 1 mod 4
          are NOT Gaussian primes: 2 ramifies as -i(1+i)^2, and p == 1 mod 4
          splits into two conjugate Gaussian primes)."""
        if isinstance(x, Zi):
            a, b = x.real, x.imag
        elif isinstance(x, int):
            a, b = x, 0
        else:
            raise TypeError("is_gaussian_prime accepts a Zi or an int")

        if a == 0 and b == 0:
            return False

        if a != 0 and b != 0:
            n = a * a + b * b
            return Zi._is_rational_prime(n)
        else:
            c = abs(a) if b == 0 else abs(b)
            return Zi._is_rational_prime(c) and c % 4 == 3

    # ---------- Number Theory ----------

    @staticmethod
    def modified_divmod(a, b):
        """Divide a by b, rounding the quotient to the nearest Gaussian
        integer (rather than truncating), so that the remainder has
        strictly smaller norm than b. This is what makes gcd/xgcd below
        terminate correctly, since Z[i] is a Euclidean domain under the
        norm only when division rounds to nearest."""
        a = Zi._ensure_zi(a)
        b = Zi._ensure_zi(b)
        if b == Zi(0, 0):
            raise ZeroDivisionError("division by zero Zi")
        q = a // b  # rounds to nearest Gaussian integer
        r = a - b * q
        return q, r

    @staticmethod
    def gcd(a, b):
        a = Zi._ensure_zi(a)
        b = Zi._ensure_zi(b)
        while b != Zi(0, 0):
            _, r = Zi.modified_divmod(a, b)
            a, b = b, r
        return a

    @staticmethod
    def xgcd(a, b):
        """Extended Euclidean algorithm. Returns (g, s, t) such that
        a*s + b*t == g == gcd(a, b) (up to a unit factor)."""
        a = Zi._ensure_zi(a)
        b = Zi._ensure_zi(b)
        old_r, r = a, b
        old_s, s = Zi(1, 0), Zi(0, 0)
        old_t, t = Zi(0, 0), Zi(1, 0)
        while r != Zi(0, 0):
            q, _ = Zi.modified_divmod(old_r, r)
            old_r, r = r, old_r - q * r
            old_s, s = s, old_s - q * s
            old_t, t = t, old_t - q * t
        return old_r, old_s, old_t

    # ---------- utilities ----------

    @staticmethod
    def random(re_min=-100, re_max=100, im_min=None, im_max=None):
        if im_min is None:
            im_min = re_min
        if im_max is None:
            im_max = re_max
        return Zi(rnd.randint(re_min, re_max), rnd.randint(im_min, im_max))

    @staticmethod
    def eye():
        return Zi(0, 1)

    @staticmethod
    def units():
        return [Zi(1), -Zi(1), Zi.eye(), -Zi.eye()]

    @property
    def is_unit(self):
        """A Gaussian integer is a unit iff it has norm 1 (equivalent to,
        but cheaper than, checking membership in Zi.units())."""
        return self.norm() == 1

    @staticmethod
    def two():
        return Zi(1, 1)
