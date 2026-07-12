"""Gaussian rational (Qi) class: a + bi with a, b in Q, represented
exactly as fractions.Fraction.

Qi is integrated with Zi (Gaussian integers): constructing a Qi whose
real and imaginary parts both happen to be whole numbers transparently
yields a Zi instead of a Qi (see __new__). This means Qi(4, 6) is
actually a Zi(4, 6), while Qi(4, '2/3') is a genuine Qi.
"""

import re
from fractions import Fraction
from math import sqrt
from numbers import Complex

from src.zi import Zi


class Qi(Complex):
    """A class that represents a Gaussian rational: a + bi with a, b in Q.
    The set of all Gaussian rationals is denoted Q(i)."""

    __slots__ = ('_real', '_imag')

    # Which character represents the imaginary unit in str(). Change via
    # Qi.set_unit_symbol('i') / Qi.set_unit_symbol('j').
    _unit_symbol = 'j'

    # Default cap used by limit_denominator() when none is given. Change
    # via Qi.set_max_denominator(...).
    _max_denominator = 1_000_000

    # A composite string like '(1/2-3/5j)', '3/5j', or '-2i': an optional
    # signed real part, an optional signed-imaginary+unit part, at least
    # one of the two required. Numbers may be plain integers, fractions
    # ("num/den"), or decimals ("3.4").
    _NUMBER = r'[+-]?\d+(?:\.\d+)?(?:/\d+)?'
    _PAIR_RE = re.compile(
        rf'^(?P<real>{_NUMBER})(?P<sign>[+-])(?P<imag>\d+(?:\.\d+)?(?:/\d+)?)[ij]$'
    )
    _IMAG_ONLY_RE = re.compile(rf'^(?P<imag>{_NUMBER})[ij]$')

    # ---------------- Construction -----------------------

    def __new__(cls, real=None, imag=None):
        r, i = Qi._coerce(real, imag)
        if r.denominator == 1 and i.denominator == 1:
            return Zi(int(r), int(i))
        return super().__new__(cls)

    def __init__(self, real=None, imag=None) -> None:
        # If __new__ returned a Zi (denominators both 1), Python does not
        # call __init__ at all, since the returned object isn't an
        # instance of Qi. So by the time we get here, we know this is a
        # genuine Qi.
        r, i = Qi._coerce(real, imag)
        super().__setattr__('_real', r)
        super().__setattr__('_imag', i)

    @staticmethod
    def _to_fraction(x):
        """Convert a single scalar component to an exact Fraction. Floats
        are converted via str() first, so Qi(2, 3.4) captures the decimal
        value 17/5 that was typed, rather than the binary floating-point
        noise you'd get from Fraction(3.4) directly."""
        if isinstance(x, Fraction):
            return x
        if isinstance(x, bool):
            return Fraction(int(x))
        if isinstance(x, int):
            return Fraction(x)
        if isinstance(x, float):
            return Fraction(str(x))
        if isinstance(x, str):
            return Fraction(x.strip())
        raise TypeError(f"Cannot convert {x!r} ({type(x).__name__}) to Fraction")

    @classmethod
    def _parse_string(cls, s):
        """Parse a full Qi string representation, e.g. '(1/2-3/5j)',
        '3/5j', '-2i', or a bare real like '4/6'. Returns a
        (Fraction, Fraction) pair. Raises ValueError if unparsable."""
        s = s.strip()
        inner = s
        if inner.startswith('(') and inner.endswith(')'):
            inner = inner[1:-1].strip()

        if inner and inner[-1] in 'ij':
            m = cls._PAIR_RE.match(inner)
            if m:
                real = Fraction(m.group('real'))
                mag = Fraction(m.group('imag'))
                imag = mag if m.group('sign') == '+' else -mag
                return real, imag
            m = cls._IMAG_ONLY_RE.match(inner)
            if m:
                return Fraction(0), Fraction(m.group('imag'))
            raise ValueError(f"Cannot parse Qi string: {s!r}")

        # No imaginary unit present: the whole thing is the real part.
        return Fraction(inner), Fraction(0)

    @staticmethod
    def _coerce(real, imag):
        """Turn constructor arguments into a (Fraction, Fraction) pair."""
        if isinstance(real, str) and imag is None:
            return Qi._parse_string(real)

        if isinstance(real, (complex, Zi, Qi)):
            if imag is not None:
                raise TypeError(
                    f"imag must be None if real is a {type(real).__name__}: {imag}"
                )
            return Qi._to_fraction(real.real), Qi._to_fraction(real.imag)

        if real is None and imag is None:
            return Fraction(0), Fraction(0)

        r = Qi._to_fraction(real) if real is not None else Fraction(0)
        i = Qi._to_fraction(imag) if imag is not None else Fraction(0)
        return r, i

    # ---------------- Accessors -----------------------

    @property
    def real(self) -> Fraction:
        return self._real

    @property
    def imag(self) -> Fraction:
        return self._imag

    def __getitem__(self, idx):
        if idx == 0:
            return self.real
        elif idx == 1:
            return self.imag
        raise IndexError("Qi index out of range (must be 0 or 1)")

    # ---------------- Type Cast -----------------------

    @staticmethod
    def _parts(x):
        """Extract a (Fraction, Fraction) pair from any operand type Qi's
        arithmetic understands (Qi, Zi, complex, Fraction, int, float).
        Returns None for anything else, so operator methods can return
        NotImplemented rather than raising."""
        if isinstance(x, Qi):
            return x.real, x.imag
        if isinstance(x, Zi):
            return Fraction(x.real), Fraction(x.imag)
        if isinstance(x, complex):
            return Qi._to_fraction(x.real), Qi._to_fraction(x.imag)
        if isinstance(x, Fraction):
            return x, Fraction(0)
        if isinstance(x, bool):
            return Fraction(int(x)), Fraction(0)
        if isinstance(x, int):
            return Fraction(x), Fraction(0)
        if isinstance(x, float):
            return Qi._to_fraction(x), Fraction(0)
        return None

    # ---------------- Equality -----------------------

    def __eq__(self, other):
        parts = Qi._parts(other)
        if parts is None:
            return NotImplemented
        or_, oi = parts
        return self.real == or_ and self.imag == oi

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    # ---------------- Univariate Methods -----------------------

    def __repr__(self):
        return f"Qi('{self.real}', '{self.imag}')"

    def __str__(self):
        """e.g. Qi('1/2', '-3/5') -> '(1/2-3/5j)'. Always shows both
        components with an explicit sign, unlike complex's str() (which
        omits the real part when it's zero); this keeps the format simple
        and unambiguous to parse back with Qi(str(q))."""
        sign = '-' if self.imag < 0 else '+'
        return f"({self.real}{sign}{abs(self.imag)}{Qi._unit_symbol})"

    def __hash__(self):
        return hash((self.real, self.imag))

    def __complex__(self):
        return complex(float(self.real), float(self.imag))

    def __abs__(self):
        return sqrt(self.norm())

    def __neg__(self):
        return Qi(-self.real, -self.imag)

    def __pos__(self):
        return self

    def __bool__(self):
        return self.real != 0 or self.imag != 0

    def conjugate(self):
        return Qi(self.real, -self.imag)

    def norm(self):
        return self.real * self.real + self.imag * self.imag

    # ---------------- Arithmetic -----------------------------

    def __add__(self, other):
        parts = Qi._parts(other)
        if parts is None:
            return NotImplemented
        or_, oi = parts
        return Qi(self.real + or_, self.imag + oi)

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        parts = Qi._parts(other)
        if parts is None:
            return NotImplemented
        or_, oi = parts
        return Qi(self.real - or_, self.imag - oi)

    def __rsub__(self, other):
        parts = Qi._parts(other)
        if parts is None:
            return NotImplemented
        or_, oi = parts
        return Qi(or_ - self.real, oi - self.imag)

    def __isub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        parts = Qi._parts(other)
        if parts is None:
            return NotImplemented
        c, d = parts
        a, b = self.real, self.imag
        return Qi(a * c - b * d, a * d + b * c)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __imul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        parts = Qi._parts(other)
        if parts is None:
            return NotImplemented
        c, d = parts
        denom = c * c + d * d
        if denom == 0:
            raise ZeroDivisionError("division by zero Gaussian rational")
        a, b = self.real, self.imag
        # (a+bi)/(c+di) = (a+bi)(c-di) / (c^2+d^2)
        return Qi((a * c + b * d) / denom, (b * c - a * d) / denom)

    def __rtruediv__(self, other):
        """other / self."""
        parts = Qi._parts(other)
        if parts is None:
            return NotImplemented
        c, d = parts
        a, b = self.real, self.imag
        denom = a * a + b * b
        if denom == 0:
            raise ZeroDivisionError("division by zero Gaussian rational")
        # (c+di)/(a+bi) = (c+di)(a-bi) / (a^2+b^2)
        return Qi((c * a + d * b) / denom, (d * a - c * b) / denom)

    def inverse(self):
        """The exact multiplicative inverse of this Gaussian rational."""
        denom = self.real * self.real + self.imag * self.imag
        if denom == 0:
            raise ZeroDivisionError("cannot invert zero Gaussian rational")
        return Qi(self.real / denom, -self.imag / denom)

    def __pow__(self, exponent):
        if not isinstance(exponent, int):
            return NotImplemented
        if exponent == 0:
            return Qi(1, 0)
        base, exp = (self, exponent) if exponent > 0 else (self.inverse(), -exponent)
        result = Qi(1, 0)
        while exp > 0:
            if exp & 1:
                result = result * base
            base = base * base
            exp >>= 1
        return result

    def __rpow__(self, base):
        # A Qi that survived construction (wasn't collapsed to a Zi) is,
        # by definition, not both real-valued and integer-valued, so a
        # well-defined integer power of `base` raised to this exponent
        # isn't supported.
        return NotImplemented

    # ---------- Array Conversion ----------

    def to_array(self):
        return [self.real, self.imag]

    @staticmethod
    def from_array(arr):
        if len(arr) != 2:
            raise ValueError("Array must have exactly two elements")
        return Qi(arr[0], arr[1])

    # ---------- Configuration ----------

    @classmethod
    def get_unit_symbol(cls):
        return cls._unit_symbol

    @classmethod
    def set_unit_symbol(cls, symbol):
        if symbol not in ('i', 'j'):
            raise ValueError("unit symbol must be 'i' or 'j'")
        cls._unit_symbol = symbol

    @classmethod
    def get_max_denominator(cls):
        return cls._max_denominator

    @classmethod
    def set_max_denominator(cls, value):
        if not isinstance(value, int) or value < 1:
            raise ValueError("max_denominator must be a positive integer")
        cls._max_denominator = value

    def limit_denominator(self, max_denominator=None):
        """Return a new Qi (or Zi, if both parts become whole numbers)
        with each component approximated by the closest fraction whose
        denominator does not exceed max_denominator (defaults to
        Qi.get_max_denominator())."""
        if max_denominator is None:
            max_denominator = Qi._max_denominator
        return Qi(self.real.limit_denominator(max_denominator),
                   self.imag.limit_denominator(max_denominator))
