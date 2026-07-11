import math
import random as _random


class Zi:
    """Gaussian integer: a + b*i, with integer a (re) and b (im)."""

    __slots__ = ('_re', '_im')

    def __init__(self, re=0, im=None):
        # Single complex argument (no im given, or im given as 0)
        if isinstance(re, complex):
            if im is not None and im != 0:
                raise ValueError(
                    "If re is complex, im must not be given (or must be 0)."
                )
            self._re = round(re.real)
            self._im = round(re.imag)
            return

        if im is None:
            im = 0

        if isinstance(re, (int, float)):
            self._re = round(re)
        else:
            raise TypeError(f"Unsupported type for re: {type(re)}")

        if isinstance(im, (int, float)):
            self._im = round(im)
        else:
            raise TypeError(f"Unsupported type for im: {type(im)}")

    # ---------- helpers ----------

    @staticmethod
    def _ensure_zi(x):
        if isinstance(x, Zi):
            return x
        if isinstance(x, complex):
            return Zi(x)
        if isinstance(x, (int, float)):
            return Zi(x, 0)
        raise TypeError(f"Cannot convert {type(x)} to Zi")

    # ---------- basic protocol ----------

    def __getitem__(self, idx):
        if idx == 0:
            return self._re
        elif idx == 1:
            return self._im
        raise IndexError("Zi index out of range (must be 0 or 1)")

    def __repr__(self):
        return f"Zi({self._re}, {self._im})"

    def __str__(self):
        if self._im == 0:
            return str(self._re)
        return str(complex(self._re, self._im))

    def __complex__(self):
        return complex(self._re, self._im)

    # ---------- arithmetic ----------

    def __add__(self, other):
        oth = Zi._ensure_zi(other)
        return Zi(self._re + oth._re, self._im + oth._im)
        # if isinstance(other, Zi):
        #     return Zi(self._re + other._re, self._im + other._im)
        # if isinstance(other, int):
        #     return Zi(self._re + other, self._im)
        # return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        oth = Zi._ensure_zi(other)
        return Zi(self._re - oth._re, self._im - oth._im)
        # if isinstance(other, Zi):
        #     return Zi(self._re - other._re, self._im - other._im)
        # if isinstance(other, int):
        #     return Zi(self._re - other, self._im)
        # return NotImplemented

    def __rsub__(self, other):
        oth = Zi._ensure_zi(other)
        return oth - self
        # if isinstance(other, int):
        # return Zi(other - self._re, -self._im)
        # return NotImplemented

    def __isub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        oth = Zi._ensure_zi(other)
        # if isinstance(other, Zi):
        a, b = self._re, self._im
        c, d = oth._re, oth._im
        return Zi(a * c - b * d, a * d + b * c)
        # if isinstance(other, int):
        #     return Zi(self._re * other, self._im * other)
        # return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __imul__(self, other):
        return self.__mul__(other)

    def __pow__(self, n):
        if not isinstance(n, int) or n < 0:
            raise TypeError("Exponent must be a non-negative integer")
        result = Zi(1, 0)
        base = self
        while n > 0:
            if n & 1:
                result = result * base
            base = base * base
            n >>= 1
        return result

    def __neg__(self):
        return Zi(-self._re, -self._im)

    def __pos__(self):
        return Zi(self._re, self._im)

    # ---------- comparisons ----------

    def __eq__(self, other):
        if isinstance(other, Zi):
            return self._re == other._re and self._im == other._im
        if isinstance(other, int):
            return self._re == other and self._im == 0
        if isinstance(other, complex):
            return self._re == other.real and self._im == other.imag
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __hash__(self):
        return hash((self._re, self._im))

    # ---------- norm / abs / floordiv / mod ----------

    def norm(self):
        return self._re * self._re + self._im * self._im

    def __abs__(self):
        return math.sqrt(self.norm())

    def __floordiv__(self, other):
        other_c = complex(Zi._ensure_zi(other))
        if other_c == 0:
            raise ZeroDivisionError("division by zero Zi")
        q = complex(self) / other_c
        return Zi(q)

    def __rfloordiv__(self, other):
        other_zi = Zi._ensure_zi(other)
        return other_zi.__floordiv__(self)

    def __mod__(self, other):
        other_zi = Zi._ensure_zi(other)
        q = self // other_zi
        return self - other_zi * q

    # ---------- properties ----------

    @property
    def real(self):
        return self._re

    @property
    def imag(self):
        return self._im

    def conj(self):
        return Zi(self._re, -self._im)

    # ---------- array conversion ----------

    def to_array(self):
        return [self._re, self._im]

    @staticmethod
    def from_array(arr):
        if len(arr) != 2:
            raise ValueError("Array must have exactly two elements")
        return Zi(arr[0], arr[1])

    # ---------- primality ----------

    @staticmethod
    def _is_rational_prime(n):
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
        if isinstance(x, Zi):
            a, b = x._re, x._im
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

    # ---------- gcd machinery ----------

    @staticmethod
    def modified_divmod(a, b):
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

    # ---------- random ----------

    @staticmethod
    def random(re_min=-10, re_max=10, im_min=None, im_max=None):
        if im_min is None:
            im_min = re_min
        if im_max is None:
            im_max = re_max
        return Zi(_random.randint(re_min, re_max), _random.randint(im_min, im_max))

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
