from abc import ABC
# from numbers import Number
from fractions import Fraction
from math import sqrt
import generic_utils as utils


class Hypercomplex(ABC):
    _unit_strings = ["1", "i", "j", "k", "L", "I", "J", "K"]

    def __init__(self, real, imag):
        self._real = real
        self._imag = imag

    @property
    def real(self):
        return self._real

    @property
    def imag(self):
        return self._imag

    def __repr__(self):
        if isinstance(self.real, (int, float, complex)):
            return f"{self.__class__.__name__}({self.real}, {self.imag})"
        elif isinstance(self.real, Fraction):
            return f"{self.__class__.__name__}('{self.real}', '{self.imag}')"
        else:
            return f"{self.__class__.__name__}({repr(self.real)}, {repr(self.imag)})"

    def __str__(self):
        coefficients = list(utils.flatten(self.to_array()))
        units = self.unit_strings()[1:]
        result = f"{coefficients[0]}"
        for idx, coef in enumerate(coefficients[1:]):
            result += f" + {coef}{units[idx]}"
        # return "'" + result + "'"
        return result

    def __add__(self, other):
        return self.__class__(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return self.__class__(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        if isinstance(other, Hypercomplex) and not isinstance(other, Hypercomplex):
            oth = self.__class__(other, None)
        else:
            oth = other
        n = self.order
        k = oth.order
        if n == k:
            a, b, c, d = self.real, self.imag, oth.real, oth.imag
            real_part = a * c - d.conjugate() * b
            imag_part = d * a + b * c.conjugate()
            return Zi(real_part, imag_part)
        elif n > k:
            return self * oth.increase_order(n)
        else:
            return self.increase_order(k) * oth

    def __hash__(self):
        return hash((self.real, self.imag, type(self)))

    def __len__(self):
        return 2

    def __getitem__(self, index):
        if isinstance(index, int):
            if index == 0:
                return self.real
            elif index == 1:
                return self.imag
            else:
                raise IndexError(f"Index {index} out of range")
        else:
            raise TypeError(f"Index {index} must be a non-negative integer")

    def __iter__(self):
        return iter((self.real, self.imag))

    def __eq__(self, other):
        if type(self) == type(other):
            return self.real == other.real and self.imag == other.imag
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __neg__(self):
        return self.__class__(-self.real, -self.imag)

    def conj(self):
        return self.__class__(self.real, -self.imag)

    def __abs__(self) -> float:
        return sqrt(self.norm)

    def __pos__(self):
        return self

    @classmethod
    def unit_strings(cls):
        return cls._unit_strings

    @property
    def order(self):
        def aux(x, d):
            if isinstance(x, (int, float, complex, Fraction, str)):
                return d
            else:
                return aux(x.real, d + 1)

        return aux(self.real, 1)

    def to_array(self):
        re, im = self
        if self.order == 1:
            result = [re, im]
        else:
            result = [re.to_array(), im.to_array()]
        return result

    @property
    def norm(self):
        return self.real * self.real + self.imag * self.imag

    @property
    def dim(self):
        return 2 ** self.order

    @property
    def first(self):
        if isinstance(self.real, (int, float, complex, Fraction)):
            return self.real
        elif isinstance(self.real, Hypercomplex):
            return self.real.first
        else:
            raise Exception(f"Cannot obtain a real component from {self}")

    def zero(self, order=1):
        if isinstance(order, int) and order >= 1:
            if order == 1:
                return self.__class__(0, 0)
            else:
                d = order - 1
                return self.__class__(self.__class__.zero(self, d), self.__class__.zero(self, d))
        else:
            raise Exception(f"Cannot create a zero with {order}")

    def increase_order(self, d: int):
        if isinstance(d, int) and d >= 1:
            n = self.order
            if n == d:
                return self
            elif n < d:
                return self.__class__(self, self.zero(n)).increase_order(d)
            else:
                raise Exception(f"Should not reach this line, {self = }, {d = }")
        else:
            raise ValueError(f"{d = }, is not an integer >= 1")


class Z(Hypercomplex):

    def __init__(self, real=0, imag=0):
        super().__init__(real, imag)


class Zi(Hypercomplex):

    def __init__(self, real: Hypercomplex = 0, imag: Hypercomplex = 0) -> None:

        re = real
        im = imag

        if isinstance(real, (int, float)):
            re = round(real)

        if isinstance(imag, (int, float)):
            im = round(imag)

        super().__init__(re, im)


class Qi(Hypercomplex):
    _max_denominator = 1_000_000

    def __init__(self, real=Fraction(0, 1), imag=Fraction(0, 1)):

        re = real
        im = imag

        if isinstance(real, (int, float, str)):
            re = Fraction(real)

        if isinstance(imag, (int, float, str)):
            im = Fraction(imag)

        super().__init__(re, im)

# Example usage and testing:
if __name__ == "__main__":

    print(f"{Zi() = }")
    print(f"{Zi(7) = }")
    print(f"{Zi(1, 2) = }")
    print(f"{Zi(Zi(1, 2), Zi(3, 4)) = }")
    print(f"{Zi(1, 2) + Zi(3, 4) = }")
    print(f"{Zi(1, 2) - Zi(3, 4) = }")
    print(f"{Zi(1, 2) * Zi(3, 4) = }")
    print(f"{(1 + 2j) * (3 + 4j) = }")
    print(f"{Zi(1, 2).norm = }")
    print(f"{-Zi(1, 2) = }")
    print(f"{Zi(1, 2).conj() = }")
    # print(f"{Zi(1, 2).abs = }")
    print(f"{Zi(1, 2).order = }")
    print(f"{Zi(1, 2).real = }")
    print(f"{Zi(1, 2).imag = }")
    print(f"{Zi(1, 2).dim = }")
    print(f"{Zi(1, 2).first = }")

    z0 = Zi(1, 2)
    print(f"\n{z0 = }")
    print(f"{z0.increase_order(3) = }")
    print()

    print(f"{Qi() = }")
    print(f"{Qi('7/8') = }")
    print(f"{Qi(3, '2/3') = }")
    print(f"{Qi(Qi('1/4', '2/3'), Qi('3/5', '4/6')) = }")
    print(f"{Qi('1/4', '2/5') + Qi('3/5', '4/5') = }")
    print(f"{Qi('1/4', '2/5') - Qi('3/5', '4/5') = }")
    print(f"{Qi('1/4', '2/5') * Qi('3/5', '4/5') = }")
    print(f"{(0.25 + 0.4j) * (0.6 + 0.8j) = }")
    print(f"{Qi('2/3', '1/2').norm = }")
    print(f"{Qi('1/3', '2/4').order = }")
    print(f"{Qi('1/3', '2/4').real = }")
    print(f"{Qi('1/3', '2/4').imag = }")
    print(f"{Qi('1/3', '2/4').dim = }")
    print(f"{Qi('1/3', '2/4').first = }")

    print(f"\n{Qi(Qi('1/4', '2/3'), Qi('3/5', '4/6')).real = }")
    print(f"{Qi(Qi('1/4', '2/3'), Qi('3/5', '4/6')).imag = }")
    print(f"{Qi(Qi('1/4', '2/3'), Qi('3/5', '4/6')).dim = }")
    print(f"{Qi(Qi('1/4', '2/3'), Qi('3/5', '4/6')).order = }")
    print(f"{Qi(Qi('1/4', '2/3'), Qi('3/5', '4/6')).norm = }")
    print(f"{Qi(Qi('1/4', '2/3'), Qi('3/5', '4/6')).conj() = }")

    q0 = Qi('1/2', '2/3')
    print(f"\n{q0 = }")
    print(f"{q0.increase_order(3) = }")
    print()
