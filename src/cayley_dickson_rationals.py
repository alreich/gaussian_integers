# Cayley-Dickson Algebra with rational components

from random import randint
from fractions import Fraction
from functools import wraps
import math

from cayley_dickson_base import CayleyDicksonBase
from cayley_dickson_integers import Zi
import generic_utils as utils

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

    def __init__(self, real=None, imag=None):

        if isinstance(real, Fraction):
            re = real
        elif isinstance(real, (str, int, float)):
            re = Fraction(real).limit_denominator(self.__max_denominator)
        elif isinstance(real, (complex, Zi)):
            re = Fraction(real.real).limit_denominator(self.__max_denominator)
        elif real is None:
            re = 0
        else:
            raise TypeError(f"{real} is not a supported type")

        if isinstance(real, (complex, Zi)):
            im = Fraction(real.imag).limit_denominator(self.__max_denominator)
        elif isinstance(imag, Fraction):
            im = imag
        elif isinstance(imag, (str, int, float)):
            im = Fraction(imag).limit_denominator(self.__max_denominator)
        elif imag is None:
            im = 0
        else:
            raise TypeError(f"{imag} is not a supported type")
        super().__init__(re, im)

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

    # def __str__(self):
    #     if self.imag < 0:
    #         return f"({self.real}{self.imag}j)"
    #     else:
    #         return f"({self.real}+{self.imag}j)"

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
        """Cayley-Dickson Construction

        Conjugation, denoted here by *, is defined recursively as:
        a* = a and (u, v)* = (u*, -v)

        Multiplication is also defined recursively as:
        (a, b) x (c, d) = (a x c  +  mu x d x b*, a* x d  +  c x b)
        where for now, mu = -1 is implicitly hardcoded, below.

        If self & other have different orders, then see the
        description of the class method, scalar_mult, for how
        multiplication works.
        """
        if not isinstance(other, Zi):
            oth = Zi(other)
        else:
            oth = other
        n = self.order()
        m = oth.order()
        # If n == m, then Cayley-Dickson multiplication
        if n == m:
            a, b, c, d = self.real, self.imag, oth.real, oth.imag
            real_part = a * c - d.conjugate() * b
            imag_part = d * a + b * c.conjugate()
            return Zi(real_part, imag_part)
        # Otherwise, scalar-like (default) or cast-first multiplication
        elif m < n:
            if Qi.__SCALAR_MULTIPLICATION:
                return Zi(self.real * oth, self.imag * oth)
            else:
                return self * oth.cast(self.order())
        elif m > n:
            if Qi.__SCALAR_MULTIPLICATION:
                return Zi(self * oth.real, self * oth.imag)
            else:
                return self.cast(oth.order()) * oth
        else:
            raise Exception(f"Multiplication should never reach this line!")

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

    # @staticmethod
    # def random(re1=-100, re2=100, im1=-100, im2=100):
    #     """Return a random Gaussian rational"""
    #     if re1 < re2 and im1 < im2 and re2 >= 1 and im2 >= 1:
    #         numerator = Zi.random(re1, re2, im1, im2)
    #         denominator = Zi.random(1, re2, 1, im2)
    #     else:
    #         raise ValueError(f"Bad range")
    #     return numerator / denominator

    def cast(self, d):
        """Return a Qi that is equivalent to this one, but has a higher order, d.
        """
        if isinstance(d, int) and d >= 1:
            if isinstance(self, (int, float)):
                return Qi.cast(Qi(self), d)
            else:
                n = self.order()
                if n == d:
                    return self
                elif n < d:
                    return Qi.cast(Qi(self, Qi.zero(n)), d)
                else:
                    raise Exception(f"Should not reach this line, {self = }, {d = }")
        else:
            raise ValueError(f"{d = }, is not an integer >= 1")

    def conjugate(self):
        """This definition works recursively."""
        return Qi(self.real.conjugate(), - self.imag)

    @property
    def inverse(self):
        conj = self.conjugate()
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

    @staticmethod
    def from_array(arr):
        flat_arr = utils.flatten(arr)
        n = len(flat_arr)
        if n == 1:
            return Qi(flat_arr[0])
        elif n == 2:
            a, b = flat_arr
            if isinstance(a, (float, int)) and isinstance(b, (float, int)):
                return Qi(a, b)
            else:
                raise ValueError(f"Can make Qi out of {arr}")
        elif utils.is_power_of_two(n):
            return Qi(Qi.from_array(flat_arr[:2]), Qi.from_array(flat_arr[2:]))
        else:
            raise ValueError(f"Can make Qi out of {arr}")

    @staticmethod
    def quaternion(quat):
        """Create a Qi of order 2 (i.e., a quaternion) from a list of 4 elements
        or a string representation of a quaternion."""
        if isinstance(quat, list) and len(quat) == 4:
            re = Qi(quat[0], quat[1])
            im = Qi(quat[2], quat[3])
            return Qi(re, im)
        # TODO: Update quaternion string parser to handle fractions
        # elif isinstance(quat, str):
        #     return Qi(Qi.parse_quaternion_string(quat))
        else:
            raise ValueError(f"Cannot create a quaternion from {quat}")

    def quaternion_to_string(self):
        unit_strs = ["", "i", "j", "k"]
        if self.is_quaternion():
            qstr = ""
            for idx, coef in enumerate(utils.flatten(self.to_array())):
                # Don't include terms with 0 coefficient
                if coef > 0:
                    if idx == 0:
                        qstr = qstr + f"{coef}{unit_strs[idx]}"
                    else:
                        qstr = qstr + f"+{coef}{unit_strs[idx]}"
                elif coef < 0:
                    qstr = qstr + f"{coef}{unit_strs[idx]}"
                else:
                    pass
            return qstr
        else:
            raise Exception(f"{self} is not a quaternion")

    def hamilton_product(self, other):
        """Multiplication of two quaternions according to the classic Hamilton product."""
        if Qi.is_quaternion(self) and Qi.is_quaternion(other):
            a1, b1, c1, d1 = utils.flatten(self.to_array())
            a2, b2, c2, d2 = utils.flatten(other.to_array())
            # See https://en.wikipedia.org/wiki/Quaternion#Hamilton_product
            a = a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2
            b = a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2
            c = a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2
            d = a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2
            return Qi(Qi(a, b), Qi(c, d))
        else:
            raise Exception(f"Both {self} and {other} must be quaternions")

    @staticmethod
    def random(size=10, order=1):
        """Return a random Qi of the given order where the lower and
        upper limits of the random numbers returned are -size & size, resp."""
        if order == 1:
            return Qi(randint(-size, size), randint(-size, size))
        else:
            d = order - 1
            return Qi(Qi.random(size, d), Qi.random(size, d))

    @staticmethod
    def random_quaternion(size=10):
        """A convenience method for testing."""
        return Qi.random(size, order=2)

    @staticmethod
    def random_octonion(size=10):
        """A convenience method for testing."""
        return Qi.random(size, order=3)

    @staticmethod
    def zero(order=1):
        """Return Qi(0, 0), or Qi(Qi(0, 0), Qi(0, 0)), or so on"""
        if isinstance(order, int) and order >= 1:
            if order == 1:
                return Qi(0, 0)
            else:
                d = order - 1
                return Qi(Qi.zero(d), Qi.zero(d))
        else:
            raise Exception(f"Cannot create a zero with {order}")

    @staticmethod
    def one(order=1):
        """Return Qi(1, 0), or Qi(Qi(1, 0), Qi(0, 0)), or so on"""
        if isinstance(order, int) and order >= 1:
            if order == 1:
                return Qi(1, 0)
            else:
                d = order - 1
                return Qi(Qi.one(d), Qi.zero(d))
        else:
            raise Exception(f"Cannot create a one with {order}")

    @staticmethod
    def eye():
        """Return i = Qi(0, 1)"""
        return Qi(0, 1)

if __name__ == "__main__":
    print("=== Qi Demo ===\n")

    print(f"{Qi() = }")
    print(f"{Qi(1) = }")
    # print(f"{Qi.zero() = }")
    # print(f"{Qi.eye() = }")
    # print(f"{Qi.two() = }")
    print(f"{Qi(2.5, 3.75) = }")
    print(f"{Qi(-2.25, 3.75) = }")
    print(f"{Qi(2.25, -3.75) = }")
    print(f"{Qi(-2.25, -3.75) = }")
    print(f"{Qi(2.25, 4) = }")
    print(f"{Qi(-2.25, 4) = }")
    print(f"{Qi(2, 3.75) = }")
    print(f"{Qi(2, -3.75) = }")
    print(f"{Qi(2.25) = }")
    print(f"{Qi(2) = }")
    print(f"{Qi((2.25 - 3.75j)) = }")
    print(f"{Qi(-3.25j) = }")

    print("\n=== End of Demo ===\n")
