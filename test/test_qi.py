"""Unit tests for the Qi (Gaussian rational) class."""

import random
import unittest
from fractions import Fraction

from src.qi import Qi
from src.zi import Zi


# ----------------------------------------------------------------------
# Construction and Fraction coercion
# ----------------------------------------------------------------------

class TestInit(unittest.TestCase):
    def test_default_is_zero(self):
        # Both components denominator 1 -> collapses to Zi.
        z = Qi()
        self.assertIsInstance(z, Zi)
        self.assertEqual((z.real, z.imag), (0, 0))

    def test_int_args_collapse_to_zi(self):
        z = Qi(3, 4)
        self.assertIsInstance(z, Zi)
        self.assertEqual((z.real, z.imag), (3, 4))

    def test_real_only_defaults_imag_zero(self):
        z = Qi(7)
        self.assertIsInstance(z, Zi)
        self.assertEqual((z.real, z.imag), (7, 0))

    def test_int_and_float_mixed_matches_spec_example(self):
        # Qi(2, 3.4) -> Qi('2', '17/5'): the float goes through str()
        # first so it captures the decimal value exactly, not binary
        # floating-point noise.
        q = Qi(2, 3.4)
        self.assertIsInstance(q, Qi)
        self.assertEqual(q.real, Fraction(2, 1))
        self.assertEqual(q.imag, Fraction(17, 5))
        self.assertEqual(repr(q), "Qi('2', '17/5')")

    def test_string_fraction_args_reduce_to_lowest_terms(self):
        # Qi('4/6', '-1/7') -> Qi('2/3', '-1/7')
        q = Qi('4/6', '-1/7')
        self.assertEqual(q.real, Fraction(2, 3))
        self.assertEqual(q.imag, Fraction(-1, 7))
        self.assertEqual(repr(q), "Qi('2/3', '-1/7')")

    def test_string_int_args(self):
        q = Qi('2', '17/5')
        self.assertEqual(q.real, Fraction(2, 1))
        self.assertEqual(q.imag, Fraction(17, 5))

    def test_string_decimal_arg(self):
        self.assertEqual(Qi._to_fraction('3.4'), Fraction(17, 5))

    def test_fraction_args_passthrough(self):
        q = Qi(Fraction(1, 2), Fraction(-2, 3))
        self.assertEqual((q.real, q.imag), (Fraction(1, 2), Fraction(-2, 3)))

    def test_float_that_reduces_to_whole_collapses_to_zi(self):
        z = Qi(2.0, 4.0)
        self.assertIsInstance(z, Zi)
        self.assertEqual((z.real, z.imag), (2, 4))

    def test_from_complex(self):
        q = Qi(1.5 + 2j)
        self.assertEqual(q.real, Fraction(3, 2))
        self.assertEqual(q.imag, Fraction(2, 1))

    def test_from_complex_with_imag_raises(self):
        with self.assertRaises(TypeError):
            Qi(1.5 + 2j, 1)

    def test_from_zi(self):
        q = Qi(Zi(3, 4))
        self.assertIsInstance(q, Zi)  # both components integral
        self.assertEqual((q.real, q.imag), (3, 4))

    def test_from_zi_with_imag_raises(self):
        with self.assertRaises(TypeError):
            Qi(Zi(3, 4), 1)

    def test_from_qi(self):
        original = Qi('1/2', '1/3')
        copy = Qi(original)
        self.assertEqual(copy, original)

    def test_from_qi_with_imag_raises(self):
        with self.assertRaises(TypeError):
            Qi(Qi('1/2', '1/3'), 1)

    def test_invalid_real_type_raises(self):
        with self.assertRaises(TypeError):
            Qi(object())

    def test_invalid_string_raises_value_error(self):
        with self.assertRaises(ValueError):
            Qi('not-a-number')

    def test_bool_component_treated_as_zero_or_one(self):
        q = Qi(True, False)
        self.assertIsInstance(q, Zi)
        self.assertEqual((q.real, q.imag), (1, 0))


# ----------------------------------------------------------------------
# Zi integration: denominator-1 collapse
# ----------------------------------------------------------------------

class TestZiCollapse(unittest.TestCase):
    def test_whole_number_components_collapse_to_zi(self):
        self.assertIsInstance(Qi(4, 6), Zi)
        self.assertNotIsInstance(Qi(4, 6), Qi)

    def test_fractional_component_stays_qi(self):
        q = Qi(4, Fraction(2, 3))
        self.assertIsInstance(q, Qi)

    def test_arithmetic_result_collapses_when_exact(self):
        result = Qi('1/2', '0') + Qi('1/2', '0')
        self.assertIsInstance(result, Zi)
        self.assertEqual(result, Zi(1, 0))

    def test_arithmetic_result_stays_qi_when_fractional(self):
        result = Qi('1/2', '0') + Qi('1/3', '0')
        self.assertIsInstance(result, Qi)
        self.assertEqual(result, Qi('5/6', '0'))

    def test_zi_truediv_returns_qi_that_collapses_when_exact(self):
        # Zi's own / operator (see test_zi.py) delegates its exact
        # quotient through Qi's constructor, so it also collapses.
        result = (Zi(1, 2) * Zi(2, 1)) / Zi(2, 1)
        self.assertIsInstance(result, Zi)
        self.assertEqual(result, Zi(1, 2))


# ----------------------------------------------------------------------
# String representation and round-trip parsing
# ----------------------------------------------------------------------

class TestStringRepresentation(unittest.TestCase):
    def test_repr_matches_spec_example(self):
        self.assertEqual(repr(Qi('1/2', '-3/5')), "Qi('1/2', '-3/5')")

    def test_str_matches_spec_example(self):
        self.assertEqual(str(Qi('1/2', '-3/5')), '(1/2-3/5j)')

    def test_str_positive_imag(self):
        self.assertEqual(str(Qi('1/2', '3/5')), '(1/2+3/5j)')

    def test_str_whole_number_real_part(self):
        # Qi(3, '1/2') isn't whole in imag, so stays Qi; real shows without
        # a denominator since Fraction's str omits it when denom == 1.
        self.assertEqual(str(Qi(3, '1/2')), '(3+1/2j)')

    def test_str_unit_symbol_configurable(self):
        Qi.set_unit_symbol('i')
        try:
            self.assertEqual(str(Qi('1/2', '-3/5')), '(1/2-3/5i)')
        finally:
            Qi.set_unit_symbol('j')

    def test_set_unit_symbol_rejects_invalid(self):
        with self.assertRaises(ValueError):
            Qi.set_unit_symbol('k')

    def test_get_unit_symbol_default(self):
        self.assertEqual(Qi.get_unit_symbol(), 'j')

    def test_round_trip_parses_own_str_output(self):
        original = Qi('1/2', '-3/5')
        self.assertEqual(Qi(str(original)), original)

    def test_round_trip_with_i_unit(self):
        Qi.set_unit_symbol('i')
        try:
            original = Qi('7/9', '-2/11')
            self.assertEqual(Qi(str(original)), original)
        finally:
            Qi.set_unit_symbol('j')

    def test_round_trip_many_random_values(self):
        rng = random.Random(42)
        for _ in range(200):
            r = Fraction(rng.randint(-50, 50), rng.randint(1, 20))
            i = Fraction(rng.randint(-50, 50), rng.randint(1, 20))
            q = Qi(r, i)
            if isinstance(q, Zi):
                continue  # collapsed; str()/parsing tested elsewhere
            self.assertEqual(Qi(str(q)), q)

    def test_parse_bare_real_fraction_string(self):
        self.assertEqual(Qi('4/6'), Qi('2/3', '0'))

    def test_parse_imaginary_only_string(self):
        self.assertEqual(Qi('-3/5j'), Qi('0', '-3/5'))
        self.assertEqual(Qi('3/5i'), Qi('0', '3/5'))

    def test_parse_with_surrounding_parens_and_no_parens(self):
        self.assertEqual(Qi('(1/2-3/5j)'), Qi('1/2', '-3/5'))
        self.assertEqual(Qi('1/2-3/5j'), Qi('1/2', '-3/5'))


# ----------------------------------------------------------------------
# Basic protocol: getitem/unpacking/hash/bool/complex
# ----------------------------------------------------------------------

class TestProtocols(unittest.TestCase):
    def test_getitem(self):
        q = Qi('1/2', '1/3')
        self.assertEqual(q[0], Fraction(1, 2))
        self.assertEqual(q[1], Fraction(1, 3))
        with self.assertRaises(IndexError):
            q[2]

    def test_unpacking(self):
        a, b = Qi('1/2', '1/3')
        self.assertEqual((a, b), (Fraction(1, 2), Fraction(1, 3)))

    def test_complex_conversion(self):
        self.assertEqual(complex(Qi('1/2', '1/4')), 0.5 + 0.25j)

    def test_bool_zero_is_falsy(self):
        self.assertFalse(Qi(0, 0))
        self.assertTrue(Qi('1/2', 0))
        self.assertTrue(Qi(0, '1/2'))

    def test_hash_equal_objects_equal_hash(self):
        self.assertEqual(hash(Qi('1/2', '1/3')), hash(Qi(Fraction(1, 2), Fraction(1, 3))))

    def test_hashable_in_set(self):
        s = {Qi('1/2', '1/3'), Qi('1/2', '1/3'), Qi('1/2', '2/3')}
        self.assertEqual(len(s), 2)


# ----------------------------------------------------------------------
# Equality
# ----------------------------------------------------------------------

class TestEquality(unittest.TestCase):
    def test_equal_qi(self):
        self.assertEqual(Qi('1/2', '1/3'), Qi('2/4', '1/3'))

    def test_not_equal_qi(self):
        self.assertNotEqual(Qi('1/2', '1/3'), Qi('1/3', '1/2'))

    def test_equal_to_zi(self):
        self.assertEqual(Qi(3, 0), 3)  # collapses; sanity
        self.assertEqual(Qi('3/1', '0'), Zi(3, 0))

    def test_equal_to_complex(self):
        self.assertEqual(Qi('1/2', '1/4'), 0.5 + 0.25j)

    def test_equal_to_int_and_float(self):
        self.assertEqual(Qi('4/1', '0'), 4)
        self.assertEqual(Qi('1/2', '0'), 0.5)

    def test_ne(self):
        self.assertTrue(Qi('1/2', '1/3') != Qi('1/3', '1/2'))
        self.assertFalse(Qi('1/2', '1/3') != Qi('2/4', '1/3'))

    def test_incomparable_type_no_raise(self):
        self.assertFalse(Qi('1/2', '1/3') == "nope")
        self.assertNotEqual(Qi('1/2', '1/3'), object())
        self.assertTrue(Qi('1/2', '1/3') != "nope")


# ----------------------------------------------------------------------
# Unary ops
# ----------------------------------------------------------------------

class TestUnary(unittest.TestCase):
    def test_neg(self):
        self.assertEqual(-Qi('1/2', '-1/3'), Qi('-1/2', '1/3'))

    def test_pos(self):
        q = Qi('1/2', '-1/3')
        self.assertEqual(+q, q)

    def test_conjugate(self):
        self.assertEqual(Qi('1/2', '1/3').conjugate(), Qi('1/2', '-1/3'))

    def test_norm(self):
        self.assertEqual(Qi('1/2', '1/2').norm(), Fraction(1, 2))

    def test_abs(self):
        self.assertAlmostEqual(abs(Qi('3/5', '4/5')), 1.0)


# ----------------------------------------------------------------------
# Addition / subtraction, including reflected and in-place operators
# ----------------------------------------------------------------------

class TestAddSub(unittest.TestCase):
    def test_add_qi(self):
        self.assertEqual(Qi('1/2', '1/3') + Qi('1/3', '1/2'), Qi('5/6', '5/6'))

    def test_add_mixed_types_both_sides(self):
        self.assertEqual(Qi('1/2', '0') + 1, Qi('3/2', '0'))
        self.assertEqual(1 + Qi('1/2', '0'), Qi('3/2', '0'))
        self.assertEqual(Qi('1/2', '0') + 0.5, Qi(1, 0))
        self.assertEqual(Qi('1/2', '1/2') + (1 + 1j), Qi('3/2', '3/2'))
        self.assertEqual(Qi('1/2', '0') + Zi(1, 1), Qi('3/2', '1'))

    def test_iadd(self):
        q = Qi('1/2', '1/3')
        q += Qi('1/3', '1/2')
        self.assertEqual(q, Qi('5/6', '5/6'))

    def test_sub_qi(self):
        self.assertEqual(Qi('1/2', '1/2') - Qi('1/3', '1/6'), Qi('1/6', '1/3'))

    def test_sub_mixed_types_both_sides(self):
        self.assertEqual(Qi('3/2', '0') - 1, Qi('1/2', '0'))
        self.assertEqual(1 - Qi('1/2', '0'), Qi('1/2', '0'))
        self.assertEqual(Zi(1, 1) - Qi('1/2', '0'), Qi('1/2', '1'))

    def test_isub(self):
        q = Qi('1/2', '1/2')
        q -= Qi('1/3', '1/6')
        self.assertEqual(q, Qi('1/6', '1/3'))


# ----------------------------------------------------------------------
# Multiplication, including reflected and in-place operators
# ----------------------------------------------------------------------

class TestMul(unittest.TestCase):
    def test_mul_qi(self):
        # (1/2+1/3i)(1/3+1/2i) = 1/6 + 1/4i + 1/9i + 1/6 i^2
        #                      = (1/6 - 1/6) + (1/4+1/9)i = 0 + 13/36 i
        self.assertEqual(Qi('1/2', '1/3') * Qi('1/3', '1/2'), Qi('0', '13/36'))

    def test_mul_mixed_types_both_sides(self):
        self.assertEqual(Qi('1/2', '1/3') * 2, Qi('1', '2/3'))
        self.assertEqual(2 * Qi('1/2', '1/3'), Qi('1', '2/3'))
        self.assertEqual(Qi('1/2', '1/3') * Zi(1, 2), Qi('-1/6', '4/3'))
        self.assertEqual(Zi(1, 2) * Qi('1/2', '1/3'), Qi('-1/6', '4/3'))

    def test_imul(self):
        q = Qi('1/2', '1/3')
        q *= Qi('1/3', '1/2')
        self.assertEqual(q, Qi('0', '13/36'))


# ----------------------------------------------------------------------
# True division, including reflected operator, inverse, and zero division
# ----------------------------------------------------------------------

class TestDivAndInverse(unittest.TestCase):
    def test_exact_division_round_trip(self):
        product = Qi('1/2', '1/3') * Qi('1/3', '1/2')
        self.assertEqual(product / Qi('1/3', '1/2'), Qi('1/2', '1/3'))

    def test_division_by_zero_raises(self):
        with self.assertRaises(ZeroDivisionError):
            Qi('1/2', '1/3') / Qi(0, 0)

    def test_rtruediv(self):
        self.assertEqual(1 / Qi('1/2', '0'), Qi(2, 0))
        self.assertEqual(2 / Qi('0', '1'), Qi('0', '-2'))

    def test_div_with_zi_operand(self):
        self.assertEqual(Qi('1', '1') / Zi(1, 1), Qi(1, 0))
        self.assertEqual(Zi(1, 1) / Qi('1', '0'), Qi(1, 1))

    def test_inverse_matches_1_over_self(self):
        q = Qi('3/5', '4/5')
        self.assertEqual(q.inverse(), 1 / q)

    def test_inverse_is_exact(self):
        q = Qi('2/7', '-3/11')
        self.assertEqual(q * q.inverse(), Qi(1, 0))

    def test_inverse_of_zero_raises(self):
        with self.assertRaises(ZeroDivisionError):
            Qi(0, 0).inverse()


# ----------------------------------------------------------------------
# Power, including reflected operator
# ----------------------------------------------------------------------

class TestPow(unittest.TestCase):
    def test_pow_zero(self):
        self.assertEqual(Qi('1/2', '1/3') ** 0, Qi(1, 0))

    def test_pow_positive(self):
        q = Qi('1/2', '1/3')
        self.assertEqual(q ** 2, q * q)
        self.assertEqual(q ** 3, q * q * q)

    def test_pow_negative_is_exact_inverse_power(self):
        q = Qi('1/2', '1/3')
        self.assertEqual(q ** -1, q.inverse())
        self.assertEqual(q ** -2, q.inverse() * q.inverse())

    def test_pow_non_int_exponent_not_implemented(self):
        self.assertIs(Qi('1/2', '1/3').__pow__(0.5), NotImplemented)

    def test_rpow_not_implemented(self):
        # A genuine Qi (post-collapse-check) can never be both real and
        # integer-valued, so base ** qi is never well-defined here.
        self.assertIs(Qi('1/2', '1/3').__rpow__(2), NotImplemented)


# ----------------------------------------------------------------------
# Array conversion
# ----------------------------------------------------------------------

class TestArrayConversion(unittest.TestCase):
    def test_to_array(self):
        self.assertEqual(Qi('1/2', '-1/3').to_array(), [Fraction(1, 2), Fraction(-1, 3)])

    def test_from_array(self):
        self.assertEqual(Qi.from_array(['1/2', '-1/3']), Qi('1/2', '-1/3'))

    def test_from_array_wrong_length_raises(self):
        with self.assertRaises(ValueError):
            Qi.from_array(['1/2'])

    def test_round_trip(self):
        q = Qi('7/9', '-2/11')
        self.assertEqual(Qi.from_array(q.to_array()), q)


# ----------------------------------------------------------------------
# max_denominator configuration and limit_denominator
# ----------------------------------------------------------------------

class TestMaxDenominator(unittest.TestCase):
    def setUp(self):
        self._orig = Qi.get_max_denominator()

    def tearDown(self):
        Qi.set_max_denominator(self._orig)

    def test_default_max_denominator(self):
        self.assertEqual(Qi.get_max_denominator(), 1_000_000)

    def test_set_and_get(self):
        Qi.set_max_denominator(500)
        self.assertEqual(Qi.get_max_denominator(), 500)

    def test_set_rejects_non_positive(self):
        with self.assertRaises(ValueError):
            Qi.set_max_denominator(0)
        with self.assertRaises(ValueError):
            Qi.set_max_denominator(-5)

    def test_set_rejects_non_int(self):
        with self.assertRaises(ValueError):
            Qi.set_max_denominator(1.5)

    def test_limit_denominator_uses_class_default(self):
        Qi.set_max_denominator(5)
        result = Qi('1/3', '2/7').limit_denominator()
        self.assertLessEqual(result.real.denominator, 5)
        self.assertLessEqual(result.imag.denominator, 5)

    def test_limit_denominator_explicit_argument_overrides_default(self):
        result = Qi('1/3', '2/7').limit_denominator(5)
        self.assertLessEqual(result.real.denominator, 5)
        self.assertLessEqual(result.imag.denominator, 5)

    def test_limit_denominator_exact_value_unchanged(self):
        q = Qi('1/3', '1/4')
        self.assertEqual(q.limit_denominator(100), q)

    def test_limit_denominator_can_collapse_to_zi(self):
        result = Qi('1000001/1000000', '0').limit_denominator(1)
        self.assertIsInstance(result, Zi)
        self.assertEqual(result, Zi(1, 0))


# ----------------------------------------------------------------------
# Fuzz tests: algebraic properties that must hold for ALL Gaussian
# rationals
# ----------------------------------------------------------------------

class TestFuzz(unittest.TestCase):
    SEED = 20260711
    N_TRIALS = 300
    COORD_RANGE = 200
    DENOM_RANGE = 20

    def setUp(self):
        self.rng = random.Random(self.SEED)

    def _random_qi(self, allow_zero=True):
        while True:
            a = Fraction(self.rng.randint(-self.COORD_RANGE, self.COORD_RANGE),
                         self.rng.randint(1, self.DENOM_RANGE))
            b = Fraction(self.rng.randint(-self.COORD_RANGE, self.COORD_RANGE),
                         self.rng.randint(1, self.DENOM_RANGE))
            if allow_zero or (a, b) != (0, 0):
                return Qi(a, b)

    def test_addition_commutative(self):
        for _ in range(self.N_TRIALS):
            a, b = self._random_qi(), self._random_qi()
            self.assertEqual(a + b, b + a)

    def test_addition_associative(self):
        for _ in range(self.N_TRIALS):
            a, b, c = (self._random_qi() for _ in range(3))
            self.assertEqual((a + b) + c, a + (b + c))

    def test_additive_identity(self):
        for _ in range(self.N_TRIALS):
            a = self._random_qi()
            self.assertEqual(a + Qi(0, 0), a)

    def test_additive_inverse(self):
        for _ in range(self.N_TRIALS):
            a = self._random_qi()
            self.assertEqual(a + (-a), Qi(0, 0))

    def test_multiplication_commutative(self):
        for _ in range(self.N_TRIALS):
            a, b = self._random_qi(), self._random_qi()
            self.assertEqual(a * b, b * a)

    def test_multiplication_associative(self):
        for _ in range(self.N_TRIALS):
            a, b, c = (self._random_qi() for _ in range(3))
            self.assertEqual((a * b) * c, a * (b * c))

    def test_multiplicative_identity(self):
        for _ in range(self.N_TRIALS):
            a = self._random_qi()
            self.assertEqual(a * Qi(1, 0), a)

    def test_distributive_law(self):
        for _ in range(self.N_TRIALS):
            a, b, c = (self._random_qi() for _ in range(3))
            self.assertEqual(a * (b + c), a * b + a * c)

    def test_norm_is_multiplicative(self):
        for _ in range(self.N_TRIALS):
            a, b = self._random_qi(), self._random_qi()
            self.assertEqual((a * b).norm(), a.norm() * b.norm())

    def test_conjugate_involution(self):
        for _ in range(self.N_TRIALS):
            a = self._random_qi()
            self.assertEqual(a.conjugate().conjugate(), a)

    def test_conjugate_norm_identity(self):
        for _ in range(self.N_TRIALS):
            a = self._random_qi()
            self.assertEqual(a * a.conjugate(), Qi(a.norm(), 0))

    def test_conjugate_of_product(self):
        for _ in range(self.N_TRIALS):
            a, b = self._random_qi(), self._random_qi()
            self.assertEqual((a * b).conjugate(), a.conjugate() * b.conjugate())

    def test_every_nonzero_element_has_exact_inverse(self):
        # The key structural difference from Zi: Q(i) is a FIELD, so
        # every nonzero element is invertible within the ring itself.
        for _ in range(self.N_TRIALS):
            a = self._random_qi(allow_zero=False)
            self.assertEqual(a * a.inverse(), Qi(1, 0))

    def test_division_is_exact_round_trip(self):
        for _ in range(self.N_TRIALS):
            a = self._random_qi()
            b = self._random_qi(allow_zero=False)
            product = a * b
            self.assertEqual(product / b, a)

    def test_radd_matches_add(self):
        for _ in range(self.N_TRIALS):
            a = self._random_qi()
            n = self.rng.randint(-100, 100)
            self.assertEqual(n + a, a + n)

    def test_rmul_matches_mul(self):
        for _ in range(self.N_TRIALS):
            a = self._random_qi()
            n = self.rng.randint(-100, 100)
            self.assertEqual(n * a, a * n)

    def test_rsub_consistent_with_neg_add(self):
        for _ in range(self.N_TRIALS):
            a = self._random_qi()
            n = self.rng.randint(-100, 100)
            self.assertEqual(n - a, -a + n)

    def test_pow_matches_repeated_multiplication(self):
        for _ in range(self.N_TRIALS // 5):
            a = self._random_qi(allow_zero=False)
            exp = self.rng.randint(0, 5)
            expected = Qi(1, 0)
            for _ in range(exp):
                expected = expected * a
            self.assertEqual(a ** exp, expected)

    def test_equality_reflexive_and_hash_stable(self):
        for _ in range(self.N_TRIALS):
            a = self._random_qi()
            self.assertEqual(a, a)
            self.assertEqual(hash(a), hash(Qi(a.real, a.imag)))

    def test_str_round_trips_through_constructor(self):
        for _ in range(self.N_TRIALS):
            a = self._random_qi()
            if isinstance(a, Zi):
                continue
            self.assertEqual(Qi(str(a)), a)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
