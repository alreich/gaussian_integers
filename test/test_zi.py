"""Unit tests for the Zi (Gaussian integer) class."""

import random
import unittest

from src.zi import Zi

# ----------------------------------------------------------------------
# Construction
# ----------------------------------------------------------------------

class TestInit(unittest.TestCase):
    def test_default_is_zero(self):
        z = Zi()
        self.assertEqual((z.real, z.imag), (0, 0))

    def test_int_args(self):
        z = Zi(3, 4)
        self.assertEqual((z.real, z.imag), (3, 4))

    def test_real_only_defaults_imag_zero(self):
        z = Zi(7)
        self.assertEqual((z.real, z.imag), (7, 0))

    def test_float_args_are_rounded(self):
        z = Zi(3.4, 4.6)
        self.assertEqual((z.real, z.imag), (3, 5))

    def test_from_complex(self):
        z = Zi(3 + 4j)
        self.assertEqual((z.real, z.imag), (3, 4))

    def test_from_complex_with_imag_raises(self):
        with self.assertRaises(TypeError):
            Zi(3 + 4j, 1)

    def test_from_zi(self):
        z = Zi(Zi(2, 5))
        self.assertEqual((z.real, z.imag), (2, 5))

    def test_from_zi_with_imag_raises(self):
        with self.assertRaises(TypeError):
            Zi(Zi(2, 5), 1)

    def test_invalid_real_type_raises(self):
        with self.assertRaises(TypeError):
            Zi("nope")

    def test_invalid_imag_type_raises(self):
        with self.assertRaises(TypeError):
            Zi(3, "nope")


# ----------------------------------------------------------------------
# Basic protocol: repr/str/hash/getitem/bool/complex
# ----------------------------------------------------------------------

class TestProtocols(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(repr(Zi(3, -4)), "Zi(3, -4)")

    def test_str_pure_real(self):
        self.assertEqual(str(Zi(5, 0)), "5")

    def test_str_complex(self):
        self.assertEqual(str(Zi(3, 4)), str(complex(3, 4)))

    def test_getitem(self):
        z = Zi(3, 4)
        self.assertEqual(z[0], 3)
        self.assertEqual(z[1], 4)
        with self.assertRaises(IndexError):
            z[2]

    def test_unpacking(self):
        a, b = Zi(3, 4)
        self.assertEqual((a, b), (3, 4))

    def test_complex_conversion(self):
        self.assertEqual(complex(Zi(3, 4)), 3 + 4j)

    def test_bool_zero_is_falsy(self):
        self.assertFalse(Zi(0, 0))
        self.assertTrue(Zi(1, 0))
        self.assertTrue(Zi(0, 1))

    def test_hash_equal_objects_equal_hash(self):
        self.assertEqual(hash(Zi(3, 4)), hash(Zi(3, 4)))

    def test_hashable_in_set(self):
        s = {Zi(1, 1), Zi(1, 1), Zi(2, 2)}
        self.assertEqual(len(s), 2)


# ----------------------------------------------------------------------
# Equality
# ----------------------------------------------------------------------

class TestEquality(unittest.TestCase):
    def test_equal_zi(self):
        self.assertEqual(Zi(3, 4), Zi(3, 4))

    def test_not_equal_zi(self):
        self.assertNotEqual(Zi(3, 4), Zi(4, 3))

    def test_equal_to_int(self):
        self.assertEqual(Zi(5, 0), 5)
        self.assertEqual(5, Zi(5, 0))

    def test_equal_to_complex(self):
        self.assertEqual(Zi(3, 4), 3 + 4j)

    def test_unequal_incomparable_type_no_raise(self):
        # Must return NotImplemented -> False, not raise.
        self.assertFalse(Zi(3, 4) == "not a number")
        self.assertNotEqual(Zi(3, 4), object())

    def test_eq_in_list_membership(self):
        self.assertIn("anything", ["anything"])  # sanity
        self.assertNotIn(Zi(3, 4), [1, 2, 3, "x", None])


# ----------------------------------------------------------------------
# Unary ops
# ----------------------------------------------------------------------

class TestUnary(unittest.TestCase):
    def test_neg(self):
        self.assertEqual(-Zi(3, -4), Zi(-3, 4))

    def test_pos(self):
        self.assertEqual(+Zi(3, -4), Zi(3, -4))

    def test_conjugate(self):
        self.assertEqual(Zi(3, 4).conjugate(), Zi(3, -4))

    def test_norm(self):
        self.assertEqual(Zi(3, 4).norm(), 25)

    def test_abs(self):
        self.assertEqual(abs(Zi(3, 4)), 5.0)


# ----------------------------------------------------------------------
# Addition / subtraction, including reflected operators
# ----------------------------------------------------------------------

class TestAddSub(unittest.TestCase):
    def test_add_zi(self):
        self.assertEqual(Zi(1, 2) + Zi(3, 4), Zi(4, 6))

    def test_add_int_both_sides(self):
        self.assertEqual(Zi(1, 2) + 5, Zi(6, 2))
        self.assertEqual(5 + Zi(1, 2), Zi(6, 2))

    def test_iadd(self):
        z = Zi(1, 2)
        z += Zi(3, 4)
        self.assertEqual(z, Zi(4, 6))

    def test_sub_zi(self):
        self.assertEqual(Zi(5, 5) - Zi(2, 1), Zi(3, 4))

    def test_sub_int_both_sides(self):
        self.assertEqual(Zi(5, 5) - 2, Zi(3, 5))
        self.assertEqual(10 - Zi(3, 4), Zi(7, -4))


# ----------------------------------------------------------------------
# Multiplication, including reflected operator
# ----------------------------------------------------------------------

class TestMul(unittest.TestCase):
    def test_mul_zi(self):
        # (1+2i)(3+4i) = 3 + 4i + 6i + 8i^2 = -5 + 10i
        self.assertEqual(Zi(1, 2) * Zi(3, 4), Zi(-5, 10))

    def test_mul_int_both_sides(self):
        self.assertEqual(Zi(1, 2) * 3, Zi(3, 6))
        self.assertEqual(3 * Zi(1, 2), Zi(3, 6))

    def test_mul_by_i(self):
        # multiplying by i rotates 90 degrees: (a+bi)*i = -b + ai
        self.assertEqual(Zi(3, 4) * Zi(0, 1), Zi(-4, 3))


# ----------------------------------------------------------------------
# Division, including reflected operator and zero division
# ----------------------------------------------------------------------

class TestDiv(unittest.TestCase):
    def test_exact_division(self):
        # (3+4i) = (1+2i)*(1-2i)? check an exact multiple instead:
        # (1+2i)*(2+1i) = 2 + i + 4i + 2i^2 = 0 + 5i
        product = Zi(1, 2) * Zi(2, 1)
        self.assertEqual(product / Zi(2, 1), Zi(1, 2))
        self.assertEqual(product / Zi(1, 2), Zi(2, 1))

    def test_rtruediv(self):
        # 4 / Zi(2, 0) should behave like ordinary division of reals
        self.assertEqual(4 / Zi(2, 0), Zi(2, 0))

    def test_division_by_zero_raises(self):
        with self.assertRaises(ZeroDivisionError):
            Zi(1, 1) / Zi(0, 0)

    def test_division_rounds_when_inexact(self):
        # 1 / (1+i) = 0.5 - 0.5i -> rounds to (0 - 0i) with banker's rounding
        result = Zi(1, 0) / Zi(1, 1)
        self.assertIsInstance(result, Zi)
        # sanity: result should be a "nearby" Gaussian integer
        self.assertLessEqual(abs(complex(result) - (0.5 - 0.5j)), 1.0)


# ----------------------------------------------------------------------
# Power, including reflected operator
# ----------------------------------------------------------------------

class TestPow(unittest.TestCase):
    def test_pow_zero(self):
        self.assertEqual(Zi(3, 4) ** 0, Zi(1, 0))

    def test_pow_positive(self):
        z = Zi(1, 1)
        self.assertEqual(z ** 2, z * z)
        self.assertEqual(z ** 3, z * z * z)

    def test_pow_one(self):
        self.assertEqual(Zi(3, 4) ** 1, Zi(3, 4))

    def test_rpow_real_exponent(self):
        self.assertEqual(2 ** Zi(3, 0), 8)

    def test_rpow_nonreal_exponent_not_implemented(self):
        self.assertIs(Zi(1, 1).__rpow__(2), NotImplemented)

    def test_pow_of_unit_negative_exponent_exact(self):
        # i is a unit: i^-1 == -i, exact (no rounding loss)
        i = Zi(0, 1)
        self.assertEqual(i ** -1, Zi(0, -1))


# ----------------------------------------------------------------------
# Fuzz tests: algebraic properties that must hold for ALL Gaussian ints
# ----------------------------------------------------------------------
class TestFuzz(unittest.TestCase):
    SEED = 20260710
    N_TRIALS = 500
    COORD_RANGE = 1000

    def setUp(self):
        self.rng = random.Random(self.SEED)

    def _random_zi(self, allow_zero=True):
        while True:
            a = self.rng.randint(-self.COORD_RANGE, self.COORD_RANGE)
            b = self.rng.randint(-self.COORD_RANGE, self.COORD_RANGE)
            if allow_zero or (a, b) != (0, 0):
                return Zi(a, b)

    def test_addition_commutative(self):
        for _ in range(self.N_TRIALS):
            a, b = self._random_zi(), self._random_zi()
            self.assertEqual(a + b, b + a)

    def test_addition_associative(self):
        for _ in range(self.N_TRIALS):
            a, b, c = (self._random_zi() for _ in range(3))
            self.assertEqual((a + b) + c, a + (b + c))

    def test_additive_identity(self):
        for _ in range(self.N_TRIALS):
            a = self._random_zi()
            self.assertEqual(a + Zi(0, 0), a)

    def test_additive_inverse(self):
        for _ in range(self.N_TRIALS):
            a = self._random_zi()
            self.assertEqual(a + (-a), Zi(0, 0))

    def test_multiplication_commutative(self):
        for _ in range(self.N_TRIALS):
            a, b = self._random_zi(), self._random_zi()
            self.assertEqual(a * b, b * a)

    def test_multiplication_associative(self):
        for _ in range(self.N_TRIALS):
            a, b, c = (self._random_zi() for _ in range(3))
            self.assertEqual((a * b) * c, a * (b * c))

    def test_multiplicative_identity(self):
        for _ in range(self.N_TRIALS):
            a = self._random_zi()
            self.assertEqual(a * Zi(1, 0), a)

    def test_distributive_law(self):
        for _ in range(self.N_TRIALS):
            a, b, c = (self._random_zi() for _ in range(3))
            self.assertEqual(a * (b + c), a * b + a * c)

    def test_norm_is_multiplicative(self):
        # N(a*b) == N(a) * N(b) -- classic Gaussian integer identity
        for _ in range(self.N_TRIALS):
            a, b = self._random_zi(), self._random_zi()
            self.assertEqual((a * b).norm(), a.norm() * b.norm())

    def test_conjugate_involution(self):
        for _ in range(self.N_TRIALS):
            a = self._random_zi()
            self.assertEqual(a.conjugate().conjugate(), a)

    def test_conjugate_norm_identity(self):
        # a * conj(a) == N(a) (a real, nonnegative Gaussian integer)
        for _ in range(self.N_TRIALS):
            a = self._random_zi()
            self.assertEqual(a * a.conjugate(), Zi(a.norm(), 0))

    def test_conjugate_of_product(self):
        for _ in range(self.N_TRIALS):
            a, b = self._random_zi(), self._random_zi()
            self.assertEqual((a * b).conjugate(), a.conjugate() * b.conjugate())

    def test_abs_squared_equals_norm(self):
        for _ in range(self.N_TRIALS):
            a = self._random_zi()
            self.assertAlmostEqual(abs(a) ** 2, a.norm(), places=6)

    def test_exact_division_round_trips(self):
        # Construct a*b deliberately so a*b / b == a exactly (no rounding).
        for _ in range(self.N_TRIALS):
            a = self._random_zi()
            b = self._random_zi(allow_zero=False)
            product = a * b
            self.assertEqual(product / b, a)
            self.assertEqual(product / a if a else Zi(0, 0),
                              b if a else Zi(0, 0))

    def test_radd_matches_add(self):
        for _ in range(self.N_TRIALS):
            a = self._random_zi()
            n = self.rng.randint(-1000, 1000)
            self.assertEqual(n + a, a + n)

    def test_rmul_matches_mul(self):
        for _ in range(self.N_TRIALS):
            a = self._random_zi()
            n = self.rng.randint(-1000, 1000)
            self.assertEqual(n * a, a * n)

    def test_rsub_consistent_with_neg_add(self):
        for _ in range(self.N_TRIALS):
            a = self._random_zi()
            n = self.rng.randint(-1000, 1000)
            self.assertEqual(n - a, -a + n)

    def test_pow_matches_repeated_multiplication(self):
        for _ in range(self.N_TRIALS // 5):  # smaller range: pow grows fast
            a = self._random_zi(allow_zero=False)
            exp = self.rng.randint(0, 6)
            expected = Zi(1, 0)
            for _ in range(exp):
                expected = expected * a
            self.assertEqual(a ** exp, expected)

    def test_equality_reflexive_and_hash_stable(self):
        for _ in range(self.N_TRIALS):
            a = self._random_zi()
            self.assertEqual(a, a)
            self.assertEqual(hash(a), hash(Zi(a.real, a.imag)))


def main():
    unittest.main()


if __name__ == "__main__":
    main()
