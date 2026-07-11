"""Gaussian integer (Zi) class: a + bi with a, b in Z.

Consolidates fixes for:
  - duplicate __radd__ definitions (dead code shadowing the real impl)
  - self._re typos (should be self._real) in __neg__, __pos__, conjugate, __str__
  - __eq__ raising TypeError instead of returning NotImplemented for
    incomparable types
  - missing/broken __rmul__, __truediv__, __rtruediv__, __pow__, __rpow__
"""
from math import sqrt
from numbers import Complex


class Zi(Complex):
    __slots__ = ('_real', '_imag')

    def __init__(self, real: (int, float, complex) = None, imag: (int, float) = None):
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

    @property
    def real(self) -> int:
        return self._real

    @property
    def imag(self) -> int:
        return self._imag

    @staticmethod
    def _ensure_zi(x):
        if isinstance(x, Zi):
            return x
        if isinstance(x, complex):
            return Zi(x)
        if isinstance(x, (int, float)):
            return Zi(x, 0)
        raise TypeError(f"Cannot convert {type(x)} to Zi")

    def __getitem__(self, idx):
        if idx == 0:
            return self.real
        elif idx == 1:
            return self.imag
        raise IndexError("Zi index out of range (must be 0 or 1)")

    def __eq__(self, other):
        try:
            oth = Zi._ensure_zi(other)
        except TypeError:
            return NotImplemented
        return self.real == oth.real and self.imag == oth.imag

    # ---------------- UNIVARIATE METHODS -----------------------

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

    def conjugate(self):
        return Zi(self._real, -self.imag)

    def norm(self):
        return self.real * self.real + self.imag * self.imag

    def __bool__(self):
        return self.real != 0 or self.imag != 0

    # ---------------- ARITHMETIC -----------------------------

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

    def __mul__(self, other):
        oth = Zi._ensure_zi(other)
        a, b = self
        c, d = oth
        return Zi(a * c - b * d, a * d + b * c)

    def __rmul__(self, other):
        oth = Zi._ensure_zi(other)
        return oth * self

    def __truediv__(self, other):
        oth = Zi._ensure_zi(other)
        n = oth.norm()
        if n == 0:
            raise ZeroDivisionError("division by zero Gaussian integer")
        num = self * oth.conjugate()
        return Zi(round(num.real / n), round(num.imag / n))

    def __rtruediv__(self, other):
        oth = Zi._ensure_zi(other)
        return oth.__truediv__(self)

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
