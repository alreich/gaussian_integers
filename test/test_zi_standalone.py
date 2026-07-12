"""Unit tests for the Zi (Gaussian integer) class."""

import random
import unittest

from src.zi_standalone import Zi

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
# Equality / inequality
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

    def test_ne_true_for_different_values(self):
        self.assertTrue(Zi(1, 2) != Zi(2, 1))
        self.assertNotEqual(Zi(1, 2).__ne__(Zi(2, 1)), NotImplemented)

    def test_ne_false_for_equal_values(self):
        self.assertFalse(Zi(1, 2) != Zi(1, 2))

    def test_ne_with_int_and_complex(self):
        self.assertFalse(Zi(5, 0) != 5)
        self.assertTrue(Zi(5, 0) != 6)
        self.assertFalse(Zi(3, 4) != (3 + 4j))

    def test_ne_incomparable_type_returns_true_not_raise(self):
        # __eq__ returns NotImplemented for these; Python's default
        # fallback treats that as "not equal", so != is True, no raise.
        self.assertTrue(Zi(3, 4) != "not a number")
        self.assertTrue(Zi(3, 4) != object())

    def test_ne_is_consistent_with_eq_for_all_pairs(self):
        rng = random.Random(1)
        for _ in range(200):
            a = Zi(rng.randint(-50, 50), rng.randint(-50, 50))
            b = Zi(rng.randint(-50, 50), rng.randint(-50, 50))
            self.assertEqual(a != b, not (a == b))


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
# Addition / subtraction, including reflected and in-place operators
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

    def test_isub(self):
        z = Zi(5, 5)
        z -= Zi(2, 1)
        self.assertEqual(z, Zi(3, 4))

    def test_isub_with_int(self):
        z = Zi(5, 5)
        z -= 2
        self.assertEqual(z, Zi(3, 5))

    def test_isub_does_not_mutate_original_object(self):
        # Zi is immutable (slots, no in-place field mutation): -= must
        # rebind the name to a new object, not alter the old one.
        original = Zi(5, 5)
        alias = original
        original -= Zi(1, 1)
        self.assertEqual(alias, Zi(5, 5))
        self.assertEqual(original, Zi(4, 4))


# ----------------------------------------------------------------------
# Multiplication, including reflected and in-place operators
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

    def test_imul(self):
        z = Zi(1, 2)
        z *= Zi(3, 4)
        self.assertEqual(z, Zi(-5, 10))

    def test_imul_with_int(self):
        z = Zi(1, 2)
        z *= 3
        self.assertEqual(z, Zi(3, 6))

    def test_imul_does_not_mutate_original_object(self):
        original = Zi(1, 2)
        alias = original
        original *= 3
        self.assertEqual(alias, Zi(1, 2))
        self.assertEqual(original, Zi(3, 6))


# ----------------------------------------------------------------------
# True division, including reflected operator and zero division
# ----------------------------------------------------------------------

class TestTrueDiv(unittest.TestCase):
    def test_exact_division(self):
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
        # 1 / (1+i) = 0.5 - 0.5i -> rounds to a nearby Gaussian integer
        result = Zi(1, 0) / Zi(1, 1)
        self.assertIsInstance(result, Zi)
        self.assertLessEqual(abs(complex(result) - (0.5 - 0.5j)), 1.0)

    def test_division_precise_for_large_coefficients(self):
        # Exercise the exact conjugate/norm path with values large enough
        # that a naive float-based division could lose precision.
        big = Zi(123_456_789, 987_654_321)
        divisor = Zi(3, 7)
        product = big * divisor
        self.assertEqual(product / divisor, big)


# ----------------------------------------------------------------------
# Floor division, modulus, and modified_divmod agreement
# ----------------------------------------------------------------------

class TestFloorDivMod(unittest.TestCase):
    def test_floordiv_matches_truediv(self):
        # By design (no natural order on Z[i]), // and / both round to the
        # nearest Gaussian integer and must always agree.
        rng = random.Random(7)
        for _ in range(200):
            a = Zi(rng.randint(-500, 500), rng.randint(-500, 500))
            b = Zi(rng.randint(-500, 500), rng.randint(-500, 500))
            if b == Zi(0, 0):
                continue
            self.assertEqual(a // b, a / b)

    def test_floordiv_exact(self):
        product = Zi(1, 2) * Zi(2, 1)
        self.assertEqual(product // Zi(2, 1), Zi(1, 2))

    def test_floordiv_by_zero_raises(self):
        with self.assertRaises(ZeroDivisionError):
            Zi(1, 1) // Zi(0, 0)

    def test_rfloordiv(self):
        self.assertEqual(4 // Zi(2, 0), Zi(2, 0))
        self.assertEqual((4 // Zi(2, 0)), (Zi(4, 0) // Zi(2, 0)))

    def test_floordiv_precise_for_large_coefficients(self):
        big = Zi(123_456_789, 987_654_321)
        divisor = Zi(3, 7)
        product = big * divisor
        self.assertEqual(product // divisor, big)

    def test_mod_exact_division_gives_zero_remainder(self):
        product = Zi(1, 2) * Zi(2, 1)
        self.assertEqual(product % Zi(2, 1), Zi(0, 0))

    def test_mod_matches_a_minus_b_times_floordiv(self):
        rng = random.Random(11)
        for _ in range(200):
            a = Zi(rng.randint(-500, 500), rng.randint(-500, 500))
            b = Zi(rng.randint(-500, 500), rng.randint(-500, 500))
            if b == Zi(0, 0):
                continue
            self.assertEqual(a % b, a - b * (a // b))

    def test_mod_by_zero_raises(self):
        with self.assertRaises(ZeroDivisionError):
            Zi(1, 1) % Zi(0, 0)


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
# Array conversion
# ----------------------------------------------------------------------

class TestArrayConversion(unittest.TestCase):
    def test_to_array(self):
        self.assertEqual(Zi(3, -4).to_array(), [3, -4])

    def test_from_array(self):
        self.assertEqual(Zi.from_array([3, -4]), Zi(3, -4))

    def test_from_array_wrong_length_raises(self):
        with self.assertRaises(ValueError):
            Zi.from_array([1])
        with self.assertRaises(ValueError):
            Zi.from_array([1, 2, 3])

    def test_round_trip(self):
        z = Zi(7, -9)
        self.assertEqual(Zi.from_array(z.to_array()), z)


# ----------------------------------------------------------------------
# Rational and Gaussian primality
# ----------------------------------------------------------------------

class TestPrimality(unittest.TestCase):
    def test_is_rational_prime_small_primes(self):
        for p in (2, 3, 5, 7, 11, 13, 97):
            self.assertTrue(Zi._is_rational_prime(p))

    def test_is_rational_prime_small_composites(self):
        for n in (0, 1, 4, 6, 8, 9, 10, 100):
            self.assertFalse(Zi._is_rational_prime(n))

    def test_is_rational_prime_negative_uses_absolute_value(self):
        self.assertTrue(Zi._is_rational_prime(-7))
        self.assertFalse(Zi._is_rational_prime(-8))

    def test_gaussian_prime_zero_is_not_prime(self):
        self.assertFalse(Zi.is_gaussian_prime(Zi(0, 0)))
        self.assertFalse(Zi.is_gaussian_prime(0))

    def test_gaussian_prime_ramified_two_is_not_prime(self):
        # 2 = -i * (1+i)^2, so the rational prime 2 is NOT a Gaussian prime.
        self.assertFalse(Zi.is_gaussian_prime(Zi(2, 0)))
        self.assertFalse(Zi.is_gaussian_prime(2))

    def test_gaussian_prime_one_plus_i_is_prime(self):
        # 1+i has norm 2, which is a rational prime -> Gaussian prime.
        self.assertTrue(Zi.is_gaussian_prime(Zi(1, 1)))

    def test_gaussian_prime_split_prime_is_not_prime(self):
        # 5 == 1 (mod 4): splits as (2+i)(2-i), so 5 itself is not prime
        # in Z[i], though 2+i and 2-i are.
        self.assertFalse(Zi.is_gaussian_prime(Zi(5, 0)))
        self.assertTrue(Zi.is_gaussian_prime(Zi(2, 1)))
        self.assertTrue(Zi.is_gaussian_prime(Zi(2, -1)))

    def test_gaussian_prime_inert_prime_is_prime(self):
        # 3 and 7 are == 3 (mod 4): they remain prime (inert) in Z[i].
        self.assertTrue(Zi.is_gaussian_prime(Zi(3, 0)))
        self.assertTrue(Zi.is_gaussian_prime(3))
        self.assertTrue(Zi.is_gaussian_prime(Zi(7, 0)))

    def test_gaussian_prime_norm_prime_off_axis(self):
        # 2+3i has norm 13, a rational prime -> Gaussian prime.
        self.assertTrue(Zi.is_gaussian_prime(Zi(2, 3)))

    def test_gaussian_prime_norm_composite_off_axis_not_prime(self):
        # 3+3i has norm 18 = 2 * 3^2, not a rational prime -> not prime.
        self.assertFalse(Zi.is_gaussian_prime(Zi(3, 3)))

    def test_is_gaussian_prime_invalid_type_raises(self):
        with self.assertRaises(TypeError):
            Zi.is_gaussian_prime("nope")


# ----------------------------------------------------------------------
# modified_divmod, gcd, xgcd
# ----------------------------------------------------------------------

class TestNumberTheory(unittest.TestCase):
    def test_modified_divmod_exact(self):
        product = Zi(1, 2) * Zi(2, 1)
        q, r = Zi.modified_divmod(product, Zi(2, 1))
        self.assertEqual(q, Zi(1, 2))
        self.assertEqual(r, Zi(0, 0))

    def test_modified_divmod_reconstructs_dividend(self):
        rng = random.Random(3)
        for _ in range(200):
            a = Zi(rng.randint(-500, 500), rng.randint(-500, 500))
            b = Zi(rng.randint(-500, 500), rng.randint(-500, 500))
            if b == Zi(0, 0):
                continue
            q, r = Zi.modified_divmod(a, b)
            self.assertEqual(b * q + r, a)

    def test_modified_divmod_remainder_norm_smaller_than_divisor(self):
        rng = random.Random(4)
        for _ in range(200):
            a = Zi(rng.randint(-500, 500), rng.randint(-500, 500))
            b = Zi(rng.randint(-500, 500), rng.randint(-500, 500))
            if b == Zi(0, 0):
                continue
            _, r = Zi.modified_divmod(a, b)
            self.assertLess(r.norm(), b.norm())

    def test_modified_divmod_by_zero_raises(self):
        with self.assertRaises(ZeroDivisionError):
            Zi.modified_divmod(Zi(1, 1), Zi(0, 0))

    def test_gcd_of_zero_and_x_is_x(self):
        self.assertEqual(Zi.gcd(Zi(0, 0), Zi(3, 4)), Zi(3, 4))

    def test_gcd_known_case(self):
        # gcd(4+2i, 1+i) -- 1+i divides 4+2i? (4+2i)/(1+i) = 3-i exactly.
        self.assertEqual((Zi(4, 2) / Zi(1, 1)), Zi(3, -1))
        g = Zi.gcd(Zi(4, 2), Zi(1, 1))
        self.assertEqual(g.norm(), Zi(1, 1).norm())

    def test_gcd_divides_both_operands(self):
        rng = random.Random(5)
        for _ in range(100):
            a = Zi(rng.randint(-200, 200), rng.randint(-200, 200))
            b = Zi(rng.randint(-200, 200), rng.randint(-200, 200))
            if a == Zi(0, 0) or b == Zi(0, 0):
                continue
            g = Zi.gcd(a, b)
            self.assertEqual(a % g, Zi(0, 0))
            self.assertEqual(b % g, Zi(0, 0))

    def test_xgcd_bezout_identity(self):
        rng = random.Random(6)
        for _ in range(100):
            a = Zi(rng.randint(-200, 200), rng.randint(-200, 200))
            b = Zi(rng.randint(-200, 200), rng.randint(-200, 200))
            if a == Zi(0, 0) or b == Zi(0, 0):
                continue
            g, s, t = Zi.xgcd(a, b)
            self.assertEqual(a * s + b * t, g)

    def test_xgcd_matches_gcd_up_to_unit(self):
        rng = random.Random(8)
        for _ in range(100):
            a = Zi(rng.randint(-200, 200), rng.randint(-200, 200))
            b = Zi(rng.randint(-200, 200), rng.randint(-200, 200))
            if a == Zi(0, 0) or b == Zi(0, 0):
                continue
            g, _, _ = Zi.xgcd(a, b)
            plain_g = Zi.gcd(a, b)
            self.assertEqual(g.norm(), plain_g.norm())

    def test_xgcd_with_zero(self):
        g, s, t = Zi.xgcd(Zi(0, 0), Zi(3, 4))
        self.assertEqual(g, Zi(3, 4))
        self.assertEqual(Zi(0, 0) * s + Zi(3, 4) * t, g)


# ----------------------------------------------------------------------
# Utilities: random, eye, units, is_unit, two
# ----------------------------------------------------------------------

class TestUtilities(unittest.TestCase):
    def test_random_within_bounds(self):
        for _ in range(200):
            z = Zi.random(-10, 10)
            self.assertIsInstance(z, Zi)
            self.assertTrue(-10 <= z.real <= 10)
            self.assertTrue(-10 <= z.imag <= 10)

    def test_random_asymmetric_bounds(self):
        for _ in range(200):
            z = Zi.random(re_min=0, re_max=5, im_min=-3, im_max=3)
            self.assertTrue(0 <= z.real <= 5)
            self.assertTrue(-3 <= z.imag <= 3)

    def test_eye(self):
        self.assertEqual(Zi.eye(), Zi(0, 1))
        self.assertEqual(Zi.eye() * Zi.eye(), Zi(-1, 0))

    def test_units(self):
        expected = {Zi(1, 0), Zi(-1, 0), Zi(0, 1), Zi(0, -1)}
        self.assertEqual(set(Zi.units()), expected)
        self.assertEqual(len(Zi.units()), 4)

    def test_is_unit_true_for_units(self):
        for u in Zi.units():
            self.assertTrue(u.is_unit)

    def test_is_unit_false_for_non_units(self):
        for z in (Zi(0, 0), Zi(2, 0), Zi(1, 1), Zi(3, 4)):
            self.assertFalse(z.is_unit)

    def test_is_unit_matches_norm_one(self):
        rng = random.Random(9)
        for _ in range(200):
            z = Zi(rng.randint(-10, 10), rng.randint(-10, 10))
            self.assertEqual(z.is_unit, z.norm() == 1)

    def test_two(self):
        self.assertEqual(Zi.two(), Zi(1, 1))
        # 1+i has norm 2 and is the Gaussian prime lying above the
        # ramified rational prime 2.
        self.assertEqual(Zi.two().norm(), 2)
        self.assertTrue(Zi.is_gaussian_prime(Zi.two()))


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

    def test_floordiv_and_mod_reconstruct_dividend(self):
        for _ in range(self.N_TRIALS):
            a = self._random_zi()
            b = self._random_zi(allow_zero=False)
            self.assertEqual(b * (a // b) + (a % b), a)

    def test_gcd_result_divides_both_operands(self):
        for _ in range(self.N_TRIALS // 5):
            a = self._random_zi(allow_zero=False)
            b = self._random_zi(allow_zero=False)
            g = Zi.gcd(a, b)
            self.assertEqual(a % g, Zi(0, 0))
            self.assertEqual(b % g, Zi(0, 0))

    def test_xgcd_bezout_identity_fuzz(self):
        for _ in range(self.N_TRIALS // 5):
            a = self._random_zi(allow_zero=False)
            b = self._random_zi(allow_zero=False)
            g, s, t = Zi.xgcd(a, b)
            self.assertEqual(a * s + b * t, g)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
