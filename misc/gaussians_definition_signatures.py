__author__ = "Alfred J. Reich, Ph.D."
__contact__ = "al.reich@gmail.com"
__copyright__ = "Copyright (C) 2024 Alfred J. Reich, Ph.D."
__license__ = "MIT"
__version__ = "1.0.0"

def to_gaussian_rational(number):
def gaussian_rational(fnc):

class Zi():

    def __init__(self, re=None, im=None):

    @property
    def real(self):

    @property
    def imag(self):

    def __repr__(self) -> str:

    def __str__(self) -> str:

    def __add__(self, other):

    def __radd__(self, other):

    def __iadd__(self, other):

    def __sub__(self, other):

    def __rsub__(self, other):

    def __isub__(self, other):

    def __mul__(self, other):  # self * other

    def __rmul__(self, other):  # other * self

    def __imul__(self, other):

    def __pow__(self, n: int, modulo=None):

    def __complex__(self) -> complex:

    def __neg__(self):

    def __eq__(self, other: Complex) -> bool:

    def __ne__(self, other) -> bool:

    @gaussian_rational
    def __truediv__(self, other):  # self / other

    @gaussian_rational
    def __rtruediv__(self, other):  # other / self

    def __floordiv__(self, other):  # self // other

    def __rfloordiv__(self, other):  # other // self

    def __mod__(self, other):

    def __hash__(self):

    def __abs__(self) -> float:

    def __pos__(self):

    def __rpow__(self, base):

    @staticmethod
    def eye():

    @staticmethod
    def units():

    @property
    def is_unit(self):

    @staticmethod
    def two():

    @property
    def conjugate(self):

    @property
    def norm(self) -> int:

    @staticmethod
    def random(re1=-100, re2=100, im1=-100, im2=100):

    def associates(self):

    def is_associate(self, other):

    def to_gaussian_rational(self):

    @staticmethod
    def norms_divide(a, b):

    @staticmethod
    def from_array(arr):

    @staticmethod
    def modified_divmod(a, b):

    @staticmethod
    def gcd(a, b, verbose=False):

    @staticmethod
    def xgcd(alpha, beta):

    @staticmethod
    def congruent_modulo(a, b, c):

    @staticmethod
    def is_relatively_prime(a, b) -> bool:

    @staticmethod
    def is_gaussian_prime(x) -> bool:

def isprime(n: int) -> bool:

class Qi():

    @classmethod
    def max_denominator(cls):

    @classmethod
    def set_max_denominator(cls, value):

    @property
    def real(self) -> Fraction:

    @property
    def imag(self) -> Fraction:

    def __repr__(self):

    def __str__(self):

    @gaussian_rational
    def __add__(self, other):

    @gaussian_rational
    def __radd__(self, other):

    @gaussian_rational
    def __sub__(self, other):

    @gaussian_rational
    def __rsub__(self, other):

    @gaussian_rational
    def __mul__(self, other):

    @gaussian_rational
    def __rmul__(self, other):

    def __pow__(self, n: int, modulo=None):  # self ** n

    @gaussian_rational
    def __truediv__(self, other):

    @gaussian_rational
    def __rtruediv__(self, other):

    def __neg__(self):

    def __complex__(self) -> complex:

    @gaussian_rational
    def __eq__(self, other: Complex) -> bool:

    @gaussian_rational
    def __ne__(self, other) -> bool:

    def __hash__(self):

    def __abs__(self) -> float:

    def __pos__(self):

    def __rpow__(self, **kwargs):

    def __round__(self) -> Zi:

    def __floor__(self) -> Zi:

    def __ceil__(self) -> Zi:

    @property
    def conjugate(self):

    @property
    def norm(self) -> Fraction:

    @staticmethod
    def random(re1=-100, re2=100, im1=-100, im2=100):

    @property
    def inverse(self):

    @staticmethod
    def eye():

    @staticmethod
    def units():

    def associates(self):

    def is_associate(self, other):

    @staticmethod
    def string_to_rational(qi_str):
