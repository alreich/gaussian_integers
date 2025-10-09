# This is Work-In-Progress

from random import randint
from math import sqrt
from numbers import Number
import regex
from generic_utils import flatten, is_power_of_two, make_int_or_float, SetClassVariable

class Zi:
    """Pairs of integers (Gaussian Integers), pairs of Gaussian integers (Quaternion Integers),
    and pairs of Quaternion integers (Octonion Integers), etc."""

    __SCALAR_MULTIPLICATION = True  # See the classmethod, scalar_mult

    def __init__(self, re=None, im=None):

        # --------------------------------------------------------
        # re is a float or int, and im is a float, int, or None

        if isinstance(re, (float, int)):
            self.__re = round(re)
            if im is None:
                self.__im = 0
            elif isinstance(im, (float, int)):
                self.__im = round(im)
            else:
                raise Exception(f"Inputs incompatible: {re} and {im}")

        # --------------------------------------------------------
        # re is a complex, and im is None, a complex, or a Zi

        elif isinstance(re, complex):
            if im is None:  #
                self.__re = round(re.real)
                self.__im = round(re.imag)
            elif isinstance(im, (complex, Zi)):
                self.__re = Zi(re)
                self.__im = Zi(im)
            else:
                raise Exception(f"Inputs incompatible: {re} and {im}")

        # --------------------------------------------------------
        # re is a Zi, and im is None, a complex, or a Zi

        elif isinstance(re, Zi):
            if im is None:
                self.__re = re.real
                self.__im = re.imag
            elif isinstance(im, (complex, Zi)):
                self.__re = Zi(re)
                self.__im = Zi(im)
            else:
                raise Exception(f"Inputs incompatible: {re} and {im}")

        # --------------------------------------------------------
        # re is a list or tuple of numbers with length equal to a
        # power of 2, and im is None, or it is a tuple or list
        # similar to the one input for re.
        elif isinstance(re, (tuple, list)):
            z = Zi.from_array(re)
            if im is None:
                self.__re = z.real
                self.__im = z.imag
            elif isinstance(im, (tuple, list)) and len(im) == len(re):
                w = Zi.from_array(im)
                self.__re = z
                self.__im = w
            else:
                raise Exception(f"Inputs incompatible: {re} and {im}")

        # --------------------------------------------------------
        # Both re and im are None

        elif re is None:
            self.__re = 0
            if im is None:
                self.__im = 0
            else:
                raise Exception(f"If re is None, then im must be None. But im = {im}")
        else:
            raise Exception(f"Unexpected combination of input types: {re} and {im}")

    @classmethod
    def scalar_mult(cls, value=None):
        """Determines how multiplication of two Zi's of different orders works.
        If scalar_mult is True, then the lower order Zi is treated like a scalar
        w.r.t. the higher order Zi, otherwise, prior to multiplication, the lower
        order Zi is cast to the same order as the higher order Zi.
        Calling scalar_mult() without an argument will simply return it's current
        value, which by default is True."""
        if value is None:
            return cls.__SCALAR_MULTIPLICATION
        elif isinstance(value, bool):
            cls.__SCALAR_MULTIPLICATION = value
            return cls.__SCALAR_MULTIPLICATION
        else:
            raise ValueError("scalar_mult must be a boolean value")

    def __repr__(self):
        """This representation method operates recursively"""
        return f"{self.__class__.__name__}({repr(self.__re)}, {repr(self.__im)})"

    def __str__(self):
        if isinstance(self, (float, int)):
            return self
        if self.is_complex():
            return str(complex(self))
        elif self.is_quaternion():
            return f"({self.quaternion_to_string()})"
        elif self.is_octonion():
            return f"({str(self.__re)}, {str(self.__im)})"
        else:
            return str(self.to_array())

    def __neg__(self):
        return Zi(- self.__re, - self.__im)

    def __eq__(self, other) -> bool:
        """Return True if this Zi equals other."""
        return (self.real == other.real) and (self.imag == other.imag)

    def __ne__(self, other) -> bool:
        """Return True if this Zi does NOT equal other."""
        return (self.real != other.real) or (self.imag != other.imag)

    def __add__(self, other):
        return Zi(self.__re + other.real, self.__im + other.imag)

    def __radd__(self, other):
        """The reflected (swapped) operand for addition: other + self"""
        return Zi(other) + self

    def __iadd__(self, other):
        """Implements the += operation: self += other"""
        return Zi(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return Zi(self.__re - other.real, self.__im - other.imag)

    def __rsub__(self, other):
        """The reflected (swapped) operand for subtraction: other - self"""
        return Zi(other) - self

    def __isub__(self, other):
        """Implements the -= operation: self -= other"""
        return Zi(self.real - other.real, self.imag - other.imag)

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
            if Zi.__SCALAR_MULTIPLICATION:
                return Zi(self.real * oth, self.imag * oth)
            else:
                return self * oth.cast(self.order())
        elif m > n:
            if Zi.__SCALAR_MULTIPLICATION:
                return Zi(self * oth.real, self * oth.imag)
            else:
                return self.cast(oth.order()) * oth
        else:
            raise Exception(f"Multiplication should never reach this line!")

    def __rmul__(self, other):
        return Zi(other) * self

    def __imul__(self, other):
        """Implements the *= operation: self *= other"""
        a = self.real
        b = self.imag
        c = round(other.real)
        d = round(other.imag)
        #return Zi(a * c - b * d, a * d + b * c)
        real_part = a * c - d * b.conjugate()
        imag_part = a.conjugate() * d + c * b
        return Zi(real_part, imag_part)

    def __complex__(self) -> complex:
        if self.order() == 1:
            return complex(self.__re, self.__im)
        else:
            raise Exception(f"Cannot create a complex from {self}")

    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise AttributeError(f"Zi's are immutable. Cannot modify {name}")
        super().__setattr__(name, value)

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

    def __hash__(self):
        """Allow this Zi to be hashed."""
        return hash((self.real, self.imag))

    def __abs__(self) -> float:
        """Returns the square root of the norm."""
        return sqrt(self.norm)

    def __pos__(self):
        return +self

    def __rpow__(self, base):
        return NotImplemented

    def __round__(self):
        if isinstance(self.real, Number) and isinstance(self.imag, Number):
            return Zi(round(self.real), round(self.imag))
        else:
            return self

    @property
    def real(self):
        return self.__re

    @property
    def imag(self):
        return self.__im

    @property
    def first(self):
        """Return the innermost first re value."""
        if isinstance(self.__re, int):
            return self.__re
        elif isinstance(self.__re, Zi):
            return self.__re.first
        else:
            raise Exception(f"Cannot create a real from {self}")

    @property
    def norm(self):
        return (self * self.conjugate()).first

    def conjugate(self):
        """This definition works recursively."""
        return Zi(self.__re.conjugate(), - self.__im)

    def order(self):
        """Order is the number levels contained in the Zi.
        That is, a Zi made up of two integers has order 1, and a Zi
        made up of two other Zi's, each of order n, has order n+1."""
        def aux(x, d):
            if isinstance(x, int):
                return d
            else:
                return aux(x.real, d + 1)
        return aux(self.__re, 1)

    def cast(self, d):
        """Return a Zi that is equivalent to this one, but has a higher order, d.
        Example: increase_order(Zi(2, -3), 2) -> Zi(Zi(2, -3), Zi(0, 0))"""
        if isinstance(d, int) and d >= 1:
            if isinstance(self, (int, float)):
                return Zi.cast(Zi(self), d)
            else:
                n = self.order()
                if n == d:
                    return self
                elif n < d:
                    return Zi.cast(Zi(self, Zi.zero(n)), d)
                else:
                    raise Exception(f"Should not reach this line, {self = }, {d = }")
        else:
            raise ValueError(f"{d = }, is not an integer >= 1")

    def is_real(self):
        return isinstance(self.__re, int) and self.__im == 0

    def is_complex(self):
        """Return True if this Zi is essentially a complex number
        That is, the re & im parts are numbers, not other Zis."""
        return self.order() == 1

    def is_quaternion(self):
        """Return True if this Zi is essentially a quaternion
        That is, the re & im parts are essentially complex numbers."""
        return self.order() == 2

    def is_octonion(self):
        """Return True if this Zi is essentially an octonion
        That is, the re & im parts are essentially quaternions."""
        return self.order() == 3

    def to_array(self):
        if isinstance(self.__re, (float, int)) and isinstance(self.__im, (float, int)):
            return [self.__re, self.__im]
        elif isinstance(self.__re, Zi) and isinstance(self.__im, Zi):
            return [self.__re.to_array(), self.__im.to_array()]
        else:
            raise Exception(f"Cannot create an array from {self}")

    @staticmethod
    def from_array(arr):
        flat_arr = flatten(arr)
        n = len(flat_arr)
        if n == 1:
            return Zi(flat_arr[0])
        elif n == 2:
            a, b = flat_arr
            if isinstance(a, (float, int)) and isinstance(b, (float, int)):
                return Zi(a, b)
            else:
                raise ValueError(f"Can make Zi out of {arr}")
        elif is_power_of_two(n):
            return Zi(Zi.from_array(flat_arr[:2]), Zi.from_array(flat_arr[2:]))
        else:
            raise ValueError(f"Can make Zi out of {arr}")

    @staticmethod
    def quaternion(quat):
        """Create a Zi of order 2 (i.e., a quaternion) from a list of 4 elements
        or a string representation of a quaternion."""
        if isinstance(quat, list) and len(quat) == 4:
            re = Zi(quat[0], quat[1])
            im = Zi(quat[2], quat[3])
            return Zi(re, im)
        elif isinstance(quat, str):
            return Zi(Zi.parse_quaternion_string(quat))
        else:
            raise ValueError(f"Cannot create a quaternion from {quat}")

    def quaternion_to_string(self):
        unit_strs = ["", "i", "j", "k"]
        if self.is_quaternion():
            qstr = ""
            for idx, coef in enumerate(flatten(self.to_array())):
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
        if Zi.is_quaternion(self) and Zi.is_quaternion(other):
            a1, b1, c1, d1 = flatten(self.to_array())
            a2, b2, c2, d2 = flatten(other.to_array())
            # See https://en.wikipedia.org/wiki/Quaternion#Hamilton_product
            a = a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2
            b = a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2
            c = a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2
            d = a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2
            return Zi(Zi(a, b), Zi(c, d))
        else:
            raise Exception(f"Both {self} and {other} must be quaternions")

    @staticmethod
    def random(size=10, order=1):
        """Return a random Zi of the given order where the lower and
        upper limits of the random numbers returned are -size & size, resp."""
        if order == 1:
            return Zi(randint(-size, size), randint(-size, size))
        else:
            d = order - 1
            return Zi(Zi.random(size, d), Zi.random(size, d))

    @staticmethod
    def random_quaternion(size=10):
        """A convenience method for testing."""
        return Zi.random(size, order=2)

    @staticmethod
    def random_octonion(size=10):
        """A convenience method for testing."""
        return Zi.random(size, order=3)

    @staticmethod
    def zero(order=1):
        """Return Zi(0, 0), or Zi(Zi(0, 0), Zi(0, 0)), or so on"""
        if isinstance(order, int) and order >= 1:
            if order == 1:
                return Zi(0, 0)
            else:
                d = order - 1
                return Zi(Zi.zero(d), Zi.zero(d))
        else:
            raise Exception(f"Cannot create a zero with {order}")

    @staticmethod
    def one(order=1):
        """Return Zi(1, 0), or Zi(Zi(1, 0), Zi(0, 0)), or so on"""
        if isinstance(order, int) and order >= 1:
            if order == 1:
                return Zi(1, 0)
            else:
                d = order - 1
                return Zi(Zi.one(d), Zi.zero(d))
        else:
            raise Exception(f"Cannot create a one with {order}")

    # --------------------------

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

    def associates(self):
        """Return a list of this Zi's three associates"""
        us = Zi.units()
        return list(map(lambda u: u * self, us[1:]))  # skip multiplying by 1

    # def is_associate(self, other):
    #     """Return True if the other Zi is an associate of this Zi
    #
    #     Otherwise, return False.
    #     """
    #     q = self // other
    #     if q:
    #         if q in Zi.units():
    #             return True
    #         else:
    #             return False
    #     else:
    #         return False

    @staticmethod
    def parse_quaternion_string(qstr):
        """Parse a quaternion string into a Zi.
        The quaternion string can be formatted in many different ways...
        * It may be normal: 1+2i-3j-4k
        * It may have missing terms: 1-3k, 2i-4k
        * It may have missing coefficients: i+j-k (they are assumed to be 1)
        * It may not be in the right order: 2i-1+3k-4j
        * The coefficients must be ints or floats: 7-2.4i+3.75j-4.0k
        * There will always be a single + or - between terms
        * All inputs must be valid with at least 1 term, and without repeated units (2j - 3j)
        """

        def make_term(tm):
            """Return a pair where the first element is one of 'real', 'i', 'j', or 'k'
            and the second element is the coefficient as a float or int. These will be
            used to update a dictionary."""

            # Pattern for a valid quaternion term that ends in i, j, or k.
            unit_term_pat = r'^[-+]?((\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)?[ijk]$'

            # The term is either associated with a unit (i,j,k) or it's 'real'
            if regex.match(unit_term_pat, tm):
                return tm[-1], make_int_or_float(tm[:-1])  # e.g., ('i', 2.3)
            else:
                return 'real', make_int_or_float(tm)  # e.g., ('real', -3.1)

        def maybe_add_coefficient(tm):
            """If a term consists of a single unit (i, j, k), then put
            a coefficient of 1 on it, otherwise just return the term."""

            if tm == 'i':
                return '1i'
            elif tm == 'j':
                return '1j'
            elif tm == 'k':
                return '1k'
            else:
                return tm

        # The strategy below is to perform a succession of simple edits on
        # the string to turn it into a 4-element array, rather than to try
        # to write some enormous, unreadable regular expression. The regex's
        # used here are already a bit difficult to read.

        # Make lowercase and remove all spaces
        q0 = qstr.lower().strip().replace(' ', '')

        # Put a coefficient of 1 in front of units where it is implied to be 1.
        q0a = q0.replace('+i', '+1i').replace('+j', '+1j').replace('+k', '+1k')
        q0b = q0a.replace('-i', '-1i').replace('-j', '-1j').replace('-k', '-1k')

        # Put single space in front of + & -
        q1 = q0b.replace('+', ' +').replace('-', ' -')

        # If scientific notation, remove the space that was added in the previous step
        q1a = q1.replace('e -', 'e-').replace('e +', 'e+')

        # Remove any space after leading parenthesis (created by the step above)
        q2 = q1a.replace('( ', '(')

        # Remove parentheses, if they exist
        q3 = q2.replace('(', '').replace(')', '').strip()

        # Split string at spaces.
        # The input string has now been transformed into a list of strings that
        # correspond to terms in the quaternion.
        q4 = q3.split()

        # Some terms are just units (i, j, k), possibly with a sign (-+)
        # Add a coefficient of 1 or -1 to those terms.
        q5 = [maybe_add_coefficient(t) for t in q4]

        # Make sure each term in the quaternion is valid
        qterm_pat = r'^[-+]?((\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)?[ijk]?$'
        for term in q5:
            mat = regex.match(qterm_pat, term)
            if mat is None:
                raise ValueError(f"{term} in {qstr} is not a valid quaternion term.")

        # Each call to make_term returns a key-value pair that can be used to
        # update the dictionary, qdict, where the key is one of 'real', 'i',
        # 'j', or 'k', and the value is the quaternion coefficient (float or int)
        # that corresponds to the key.
        q6 = [make_term(t) for t in q5]
        qdict = {'real': 0, 'i': 0, 'j': 0, 'k': 0}
        for term in q6:
            qdict[term[0]] = term[1]

        return list(qdict.values())

class SetScalarMult(SetClassVariable):

    def __init__(self, new_value):
        super().__init__(Zi.scalar_mult, new_value)

    def __enter__(self):
        super().__enter__()
        print(f"NOTE: Scalar Multiplication set to {self.new_value}")