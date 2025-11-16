# Cayley-Dickson Algebra with integer components

from random import randint
from math import sqrt
from numbers import Number
import numpy as np
import re as reg  # Because 're' is used often here as an abbreviation for 'real'

import generic_utils as utils
from cayley_dickson_base import CayleyDicksonBase

class Zi(CayleyDicksonBase):
    """Cayley-Dickson Algebra with integer components"""

    # TODO: Allow hypercomplex strings as input also
    def __init__(self, real=None, imag=None):

        _re, _im = None, None

        if isinstance(real, float):
            _re = int(round(real))
            if isinstance(imag, float):
                _im = int(round(imag))
            elif isinstance(imag, int):
                _im = imag
            elif imag is None:
                _im = 0
            else:
                raise TypeError(f"A float real value is not compatible with imag={imag}")

        elif isinstance(real, int):
            _re = real
            if isinstance(imag, float):
                _im = round(imag)
            elif isinstance(imag, int):
                _im = imag
            elif imag is None:
                _im = 0
            else:
                raise TypeError(f"An integer real value is not compatible with imag={imag}")

        elif isinstance(real, complex):
            # TODO: Why can't I code this like I did for real is Zi, below?
            if imag is not None:
                _re = Zi(real)
            if isinstance(imag, complex):
                _im = Zi(imag)
            elif isinstance(imag, Zi):
                _im = imag
            elif isinstance(imag, (tuple, list)):
                _im = Zi.from_array(imag)
            elif imag is None:
                _re = round(real.real)
                _im = round(real.imag)
            else:
                raise TypeError(f"A complex real value is not compatible with imag={imag}")

        elif isinstance(real, Zi):
            if imag is not None:
                _re = real
            if isinstance(imag, complex):
                _im = Zi(imag)
            elif isinstance(imag, Zi):
                _im = imag
            elif isinstance(imag, (tuple, list)):
                _im = Zi.from_array(imag)
            elif imag is None:
                _re = round(real.real)
                _im = round(real.imag)
            else:
                raise TypeError(f"A Zi real value is not compatible with imag={imag}")

        elif isinstance(real, (tuple, list)):
            _re = Zi.from_array(real)
            if isinstance(imag, complex):
                _im = Zi(imag)
            elif isinstance(imag, Zi):
                _im = imag
            elif isinstance(imag, (tuple, list)):
                _im = Zi.from_array(imag)
            elif imag is None:
                _re = round(real[0])
                _im = round(real[1])
            else:
                raise TypeError(f"A tuple or list real value is not compatible with imag={imag}")

        elif isinstance(real, str):
            _re = Zi.from_array(hypercomplex_string_to_array(real))
            if isinstance(imag, str):
                _im = Zi.from_array(hypercomplex_string_to_array(imag))
            elif isinstance(imag, complex):
                _im = Zi(imag)
            elif isinstance(imag, Zi):
                _im = imag
            elif isinstance(imag, (tuple, list)):
                _im = Zi.from_array(imag)
            elif imag is None:
                a, b = _re
                _re = a
                _im = b
            else:
                raise TypeError(f"A string real value is not compatible with imag={imag}")

        elif real is None and imag is None:
            _re = 0
            _im = 0

        else:
            raise TypeError(f"real={real} is not a valid type for creating a Zi.")

        if (isinstance(_re, int) and isinstance(_im, int)) or (_re.order == _im.order):
            super().__init__(_re, _im)
        else:
            raise TypeError(f"Inputs must resolve to two ints or two Zi's of equal order.")

    def __str__(self):
        """Return the string representation of the Zi using the current list of unit_strings."""

        result = ""  # Start with an empty string, and add to it as we go

        # If this is a complex (order=1), quaternion (order=2), or octonion (order=3),
        # then use the current value of Zi.unit_strings
        if self.order <= 3:
            unit_str = Zi.unit_strings.current
        # Otherwise, generate a list of generic unit strings
        else:
            generic_unit_strings = utils.generate_unit_strings(size = self.order ** 2)
            unit_str = Zi.unit_strings.new(generic_unit_strings)

        for idx, coef in enumerate(list(utils.flatten(self.to_array()))):

            # Handle the first element, i.e., the real part, of the hypercomplex number
            if idx == 0:
                if coef == 0:
                    if Zi.include_zero_coefs():
                        result = '0'
                    else:
                        pass  # Don't include the real part if it's zeroa
                else:
                    result = str(coef)

            # Handle the remainder of the hypercomplex number
            else:
                if coef > 0:
                    if coef == 1:
                        # If coef is +1 and nothing has been appended to the result yet,
                        # then begin the result with just the corresponding unit string.
                        if result == "":
                            result = f"{unit_str[idx]}"
                        # Otherwise, 'add' just the corresponding unit string to the result.
                        else:
                            result += f"+{unit_str[idx]}"
                    else:
                        # Else, if the coef is positive, not 1, and nothing has been appended
                        # to the result yet, then begin the result with the coef & corresponding
                        # unit string.
                        if result == "":
                            result = f"{coef}{unit_str[idx]}"
                        # Otherwise, 'add' the coef & the corresponding unit string to the result.
                        else:
                            result += f"+{coef}{unit_str[idx]}"
                # Include a zero coef depending on the value returned by 'include_zero_coef()'
                elif coef == 0:
                    if Zi.include_zero_coefs():
                        result += f"+0{unit_str[idx]}"
                # The logic below is similar to that for the 'coef > 0' case above, except simpler
                # because we always include the negative sign.
                elif coef < 0:
                    if coef == -1:
                        result += f"-{unit_str[idx]}"
                    else:
                        result += f"{coef}{unit_str[idx]}"
                else:
                    pass
        # If the result is still the empty string, then return '0'; otherwise, return the result.
        if result == "":
            return '0'
        else:
            return result

    def __neg__(self):
        return Zi(- self.real, - self.imag)

    def __add__(self, other):
        return Zi(self.real + other.real, self.imag + other.imag)

    def __radd__(self, other):
        """The reflected (swapped) operand for addition: other + self"""
        return Zi(other) + self

    def __iadd__(self, other):
        """Implements the += operation: self += other"""
        return Zi(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return Zi(self.real - other.real, self.imag - other.imag)

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
        n = self.order
        m = oth.order
        # If n == m, then Cayley-Dickson multiplication
        if n == m:
            a, b, c, d = self.real, self.imag, oth.real, oth.imag
            real_part = a * c - d.conjugate() * b
            imag_part = d * a + b * c.conjugate()
            return Zi(real_part, imag_part)
        # Otherwise, scalar-like (default) or increase_order first multiplication
        elif n > m:
            if Zi.use_scalar_mult():
                return Zi(self.real * oth, self.imag * oth)
            else:
                return self * oth.increase_order(self.order)
        elif n < m:
            if Zi.use_scalar_mult():
                return Zi(self * oth.real, self * oth.imag)
            else:
                return self.increase_order(oth.order) * oth
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
        real_part = a * c - d * b.conjugate()
        imag_part = a.conjugate() * d + c * b
        return Zi(real_part, imag_part)

    # # @gaussian_rational
    # def __truediv__(self, other):  # self / other
    #     """Divide self by other, exactly, and return the resulting Gaussian rational or integer.
    #
    #     The divisor (other) is first cast into a Gaussian rational (Qi) prior to division.
    #     """
    #     return Qi(self) / other  # Despite the Qi, this could still output a Zi
    #
    # # @gaussian_rational
    # def __rtruediv__(self, other):  # other / self
    #     """Divide pother by self, exactly, and return the resulting Gaussian rational or integer.
    #
    #     The dividend (other) is first cast into a Gaussian rational (Qi) prior to division.
    #     """
    #     return other / Qi(self)

    def __floordiv__(self, other):  # self // other
        """Implements the // operator using 'round', instead of 'floor'.

        Returns the closest integer approximation to the quotient, self / other,
        as a Zi, by rounding the real and imag parts after division, not flooring.
        'other' can be an int, float, complex, or Zi.
        """
        if isinstance(other, (int, float, complex, Zi)):
            return Zi(complex(self) / complex(other))
        else:
            raise TypeError(f"{other} is not a supported type.")

    def __rfloordiv__(self, other):  # other // self
        if isinstance(other, (int, float, complex)):
            return Zi(complex(other) / complex(self))
        else:
            raise TypeError(f"{other} is not a supported type.")

    # def __mod__(self, other):
    #     """Implements the % operator.
    #
    #     Returns the remainder of the result from modified_divmod
    #     """
    #     if isinstance(other, (int, float, complex)):
    #         oth = Zi(other)
    #     else:
    #         oth = other
    #     _, r = Zi.modified_divmod(self, oth)
    #     return r

    def __complex__(self) -> complex:
        if self.order == 1:
            return complex(self.real, self.imag)
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

    def conjugate(self):
        """This definition works recursively."""
        return Zi(self.real.conjugate(), - self.imag)

    def increase_order(self, d: int):
        if isinstance(d, int) and d >= 1:
            n = self.order
            if n == d:
                return self
            elif n < d:
                return Zi(self, Zi.zero(n)).increase_order(d)
            else:
                raise Exception(f"Should not reach this line, {self = }, {d = }")
        else:
            raise ValueError(f"{d = }, is not an integer >= 1")

    @staticmethod
    def from_array(arr):
        flat_arr = list(utils.flatten(arr))
        n = len(flat_arr)
        if n == 1:
            return Zi(flat_arr[0])
        elif n == 2:
            a, b = flat_arr
            if isinstance(a, (float, int)) and isinstance(b, (float, int)):
                return Zi(a, b)
            else:
                raise ValueError(f"Can't make Zi out of {arr}")
        elif utils.is_power_of_two(n):
            k = int(n / 2)
            return Zi(Zi.from_array(flat_arr[:k]), Zi.from_array(flat_arr[k:]))
        else:
            raise ValueError(f"Can't make Zi out of {arr}")

    @staticmethod
    def from_string(s):
        return Zi.from_array(hypercomplex_string_to_array(s))

    @staticmethod
    def quaternion(quat):
        """Create a Zi of order 2 (i.e., a quaternion) from a list of 4 elements
        or a string representation of a quaternion."""
        if isinstance(quat, list) and len(quat) == 4:
            _re = Zi(quat[0], quat[1])
            _im = Zi(quat[2], quat[3])
            return Zi(_re, _im)
        elif isinstance(quat, str):
            return Zi(hypercomplex_string_to_array(quat))
        else:
            raise ValueError(f"Cannot create a quaternion from {quat}")

    def hamilton_product(self, other):
        """Multiplication of two quaternions according to the classic Hamilton product.
        For verification purposes."""
        # The following code will work without the restriction to quaternions, as long as the
        # two inputs have the same order. So, for example, two octonions can be "multiplied"
        # like this -- the a, b, c, & d values would be complexes (Zi's). However, the resulting
        # product will not match the corresponding cayley-dickson product for octonions.
        # TODO: Generalize the Hamilton product to handle this.
        if self.is_quaternion and other.is_quaternion:
            # Decompose each quaternion into its component complex values (e.g., Zi's)
            z0, z1 = self
            z2, z3 = other
            # then decompose each complex (Zi) into its real (int) values
            a1, b1 = z0
            c1, d1 = z1
            a2, b2 = z2
            c2, d2 = z3
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

def hypercomplex_string_to_array(qs):

    # Remove spaces, add '-1' or '+1' whenever '-' or '+' are not followed by a number,
    # and add '1' to a lone 'i', 'j', or 'k', at the front of the string.
    qstr = qs.strip().replace(' ', '')
    # qstr = reg.sub('[-](?![0-9])','-1', qstr)
    qstr = reg.sub('-(?![0-9])','-1', qstr)
    qstr = reg.sub('[+](?![0-9])','+1', qstr)
    qstr = reg.sub(r"^([ijkLIJK])", r"1\1", qstr)

    # Construct a dictionary of terms with keys, 'i', 'j', and 'k'.
    # However, this does not find the real term, if it exists.
    unit_term_pat = r'[-+]?((\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)?[ijkLIJK]'
    terms = []
    term_dict = {'real': 0, 'i': 0, 'j': 0, 'k': 0, 'L': 0, 'I': 0, 'J': 0, 'K': 0}
    for match in reg.finditer(unit_term_pat, qstr):
        term = match.group(0)
        terms.append(term)
        term_dict[term[-1:]] = utils.make_int_or_float(term[:-1])

    # Use the process of elimination to identify the real term.
    for tm in terms:
        qstr = qstr.replace(tm, '')
    if qstr != '':
        term_dict['real'] = utils.make_int_or_float(qstr)

    # Convert the dictionary into an ordered list of coefficients.
    # The length of the list returned depends on what type of string
    # was input (complex, quaternion, octonion, etc.)
    result = list(term_dict.values())
    if all(x == 0 for x in result[4:]):
        if all(x == 0 for x in result[2:4]):
            return result[:2]  # complex (2 elements)
        else:
            return result[:4]  # quaternion (4 elements)
    else:
        return result  # octonion (8 elements)

def print_unit_mult_table(order, prefix=None):
    """Derive and print a units multiplication table of a given
    order. e.g., order=3 produces the table in Wikipedia, shown
    here https://en.wikipedia.org/wiki/Octonion#Multiplication"""

    dim = 2 ** order

    if dim <= 8:
        if prefix is None:
            unit_strs = Zi.unit_strings.current
        else:
            unit_strs = utils.generate_unit_strings(prefix='e', size=dim)
    else:
        if prefix is None:
            unit_strs = utils.generate_unit_strings(prefix='e', size=dim)
        else:
            unit_strs = utils.generate_unit_strings(prefix=prefix, size=dim)

    # if dim > 8:
    #     unit_strs = utils.generate_unit_strings(prefix='e', size=dim)
    # else:
    #     if prefix is None:
    #         unit_strs = Zi.unit_strings.current
    #     else:
    #         unit_strs = utils.generate_unit_strings(prefix=prefix, size=dim)

    # Create a dictionary of units, where
    # Key = unit name (str)
    # Value = unit element (Zi)
    units = dict()
    for pos in range(dim):
        arr = np.zeros(dim, dtype=int)
        arr[pos] = 1
        # units['e' + str(pos)] = Zi.from_array(list(arr.data))
        units[unit_strs[pos]] = Zi.from_array(list(arr.data))

    # Create a reverse dictionary from the one above,
    # then create a reverse dictionary of the negative units,
    # and use that to augment the original reverse dictionary
    rev = {val: key for key, val in units.items()}
    negs = {-z: '-' + e for z, e in rev.items()}
    rev.update(negs)

    # Extract a list of the unit names (str)
    unit_names = list(units.keys())

    # Print the table's column headings
    colwidth = len(unit_names[-1]) + 1
    header = f"{' ':>{colwidth}} |"
    for x in unit_names:
        header += f"{x:>{colwidth}} "
    print(header)
    # print("-"*(dim + 1)*(colwidth + 1))
    print("-"*colwidth + "-+" + "-"*dim*(colwidth + 1))

    # Print the table's rows
    for x in unit_names:
        row = f"{x:>{colwidth}} |"
        for y in unit_names:
            prod = rev[units[x] * units[y]]
            row += f"{prod:>{colwidth}} "
        print(row)

    return None

# Example usage and testing:
if __name__ == "__main__":

    print("\n=== Zi Demo ===")
    print("\nThe class Zi represents a hypercomplex integer.")
    print("(e.g., complex, quaternion, octonion, etc. with integer components)\n")

    print(f"{repr(Zi(1, 2))}, at the lowest 'level' (order=1) it's a Gaussian integer")
    print(f"\n*** Zi in string form uses 'i' instead of Python's 'j':")
    print(f"{str(Zi(1, 2)) = }")
    print(f"*** Zi can convert that string back into a Gaussian integer:")
    print(f"{Zi('1+2i') = }")
    print(f"*** But Zi will convert a Python complex string into a quaternion:")
    print(f"{Zi('1+2j') = } = 1+0i+2j+0k\n")
    print(f"{Zi() = }")
    print(f"{Zi(1) = }")
    print(f"{Zi(2) = }")
    print(f"{Zi.zero() = }")
    print(f"{Zi.eye() = }")
    print(f"{Zi.two() = }")
    print(f"\n*** Floats get rounded;")
    print(f"{Zi(2.3, 3.8) = }")
    print(f"{Zi(2, 3.8) = }")
    print(f"{Zi(2.3) = }")
    print(f"\n*** Complexes become Zi's of order 1:")
    print(f"{Zi((2.3 - 3.7j)) = }")
    print(f"{Zi(-3.3j) = }")
    print(f"{Zi(3, 7).order = }")
    print(f"{Zi(3, 7).dim = }")
    print(f"{Zi(3, 7).norm = }")
    print(f"{Zi.two().norm = }")
    print(f"{Zi(3, 7).conjugate() = }")
    print(f"{str(Zi(2, 3)) = }")
    print(f"{Zi(3, 7).conjugate() = }")
    print(f"{Zi(3, 7).to_array() = }")

    print("\nQuaternions:")
    print(f"{Zi(Zi(1, 2), Zi(3, 4)) = }")
    print(f"{str(Zi(Zi(1, 2), Zi(3, 4))) = }")
    print(f"{Zi(Zi(1, 2), Zi(3, 4)).order = }")
    print(f"{Zi(Zi(1, 2), Zi(3, 4)).dim = }")
    print(f"{Zi(Zi(1, 2), Zi(3, 4)).conjugate() = }")
    print(f"{Zi(Zi(1, 2), Zi(3, 4)).to_array() = }")

    print("\nOctonions:")
    print(f"{Zi(Zi(Zi(1, 2), Zi(3, 4)), Zi(Zi(-1, -2), Zi(-3, -4))) = }")
    print(f"{str(Zi(Zi(Zi(1, 2), Zi(3, 4)), Zi(Zi(-1, -2), Zi(-3, -4)))) = }")

    print("\nOctonion unit element multiplication table:")
    print("(see https://en.wikipedia.org/wiki/Octonion#Multiplication)")
    print("(Also Table 5 near the bottom of this webpage http://tamivox.org/eugene/octonion480/index.html)")
    print_unit_mult_table(3, prefix='e')
    print("\nor with default unit elements")
    print_unit_mult_table(3)

    print("\n=== End of Demo ===\n")
