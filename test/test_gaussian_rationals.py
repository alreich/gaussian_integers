from unittest import TestCase
from gaussians import Zi, Qi
from fractions import Fraction
from random import seed


class TesQi(TestCase):

    def setUp(self) -> None:
        self.q1 = Qi(2, 3.4)

        self.f1 = Fraction(1, 2)
        self.f2 = Fraction(3, 5)
        self.q2 = Qi(self.f1, self.f2)

        self.q3 = Qi("4/6", "-1/7")

        self.c1 = (2.2 - 7.4j)
        self.q4 = Qi(self.c1)

        self.z1 = Zi(-2, 3)
        self.q5 = Qi(self.z1)

    def testConstructor(self):
        self.assertEqual(self.q1, Qi(2, '17/5'))
        self.assertEqual(self.q2, Qi('1/2', '3/5'))
        self.assertEqual(self.q3, Qi('2/3', '-1/7'))  # 4/6 --> 2/3
        self.assertEqual(self.q4, Qi('11/5', '-37/5'))
        self.assertEqual(self.q5, Qi(-2, 3))

    def test_max_denominator(self):
        self.assertEqual(Qi.max_denominator(), 1000000)

    # def test_set_max_denominator(self):
    #     assert False

    def test_real(self):
        self.assertEqual(self.q1.real, Fraction(2, 1))

    def test_imag(self):
        self.assertEqual(self.q1.imag, Fraction(17, 5))

    def test_conjugate(self):
        self.assertEqual(self.q1.conjugate, Qi(2, '-17/5'))

    def test_str(self):
        self.assertEqual(str(self.q1), '(2+17/5j)')
        self.assertEqual(str(self.q2), '(1/2+3/5j)')
        self.assertEqual(str(self.q3), '(2/3-1/7j)')

    def test_string_to_rational(self):
        self.assertEqual(Qi.string_to_rational('(1/2+3/5j)'), Qi('1/2', '3/5'))
        self.assertEqual(Qi.string_to_rational('(1/2-3/5j)'), Qi('1/2', '-3/5'))
        self.assertEqual(Qi.string_to_rational('(-1/2+3/5j)'), Qi('-1/2', '3/5'))
        self.assertEqual(Qi.string_to_rational('(-1/2-3/5j)'), Qi('-1/2', '-3/5'))
        self.assertEqual(Qi.string_to_rational('(+1/2+3/5j)'), Qi('1/2', '3/5'))
        self.assertEqual(Qi.string_to_rational('(+1/2-3/5j)'), Qi('1/2', '-3/5'))

        self.assertEqual(Qi.string_to_rational('(1/2+3j)'), Qi('1/2', 3))
        self.assertEqual(Qi.string_to_rational('(1-3/5j)'), Qi(1, '-3/5'))
        self.assertEqual(Qi.string_to_rational('(+1-3/5j)'), Qi(1, '-3/5'))
        self.assertEqual(Qi.string_to_rational('(-2+5j)'), Qi(-2, 5))
        self.assertEqual(Qi.string_to_rational('(-1-3j)'), Qi(-1, -3))
        self.assertEqual(Qi.string_to_rational('(+2+5j)'), Qi(2, 5))
        self.assertEqual(Qi.string_to_rational('(+1-3j)'), Qi(1, -3))

    def test_addition(self):
        self.assertEqual(self.q1 + self.q2, Qi('5/2', 4))

        self.assertEqual(self.q1 + 1, Qi(3, '17/5'))
        self.assertEqual(self.q1 + 1, Qi(3, '17/5'))

        self.assertEqual(self.q1 + 1.5, Qi('7/2', '17/5'))
        self.assertEqual(1.5 + self.q1, Qi('7/2', '17/5'))

        self.assertEqual(self.q1 + (1.5 + 2j), Qi('7/2', '27/5'))
        self.assertEqual((1.5 + 2j) + self.q1, Qi('7/2', '27/5'))

    def test_subtraction(self):
        self.assertEqual(self.q1 - self.q2, Qi('3/2', '14/5'))

        self.assertEqual(self.q1 - 1, Qi(1, '17/5'))
        self.assertEqual(1 - self.q1, Qi(-1, '-17/5'))

        self.assertEqual(self.q1 - 1.5, Qi('1/2', '17/5'))
        self.assertEqual(1.5 - self.q1, Qi('-1/2', '-17/5'))

        self.assertEqual(self.q1 - (1.5 + 2j), Qi('1/2', '7/5'))
        self.assertEqual((1.5 + 2j) - self.q1, Qi('-1/2', '-7/5'))

    def test_multiplication(self):
        self.assertEqual(self.q1 * self.q2, Qi('-26/25', '29/10'))

        self.assertEqual(self.q1 * 2, Qi(4, '34/5'))
        self.assertEqual(2 * self.q1, Qi(4, '34/5'))

        self.assertEqual(self.q1 * 2.2, Qi('22/5', '187/25'))
        self.assertEqual(2.2 * self.q1, Qi('22/5', '187/25'))

        self.assertEqual(self.q1 * (2.2 - 3.6j), Qi('416/25', '7/25'))
        self.assertEqual((2.2 - 3.6j) * self.q1, Qi('416/25', '7/25'))

    def test_inverse(self):
        self.assertEqual(self.q1.inverse, Qi('50/389', '-85/389'))

    def test_division(self):
        a = self.q1
        self.assertEqual(a / self.q2, Qi('304/61', '50/61'))
        self.assertEqual(a / 2, Qi('1', '17/10'))
        self.assertEqual(2 / a, Qi('100/389', '-170/389'))
        self.assertEqual(a / 2.4, Qi('5/6', '17/12'))
        self.assertEqual(2.4 / a, Qi('120/389', '-204/389'))
        self.assertEqual(a / Zi(7, -6), Qi('-32/425', '179/425'))
        self.assertEqual(Zi(7, -6) / a, Qi('-160/389', '-895/389'))
        self.assertEqual(Zi(2, 6) / Zi(4, 5), Qi('38/41', '14/41'))

    def test_power(self):
        self.assertEqual(self.q1 ** 3, Qi('-1534/25', '187/125'))

    def test_norm(self):
        self.assertEqual(self.q1.norm, Fraction(389, 25))

    def test_negation(self):
        self.assertEqual(-self.q2, Qi('-1/2', '-3/5'))

    def test_equality(self):
        self.assertTrue(self.q1 == Qi(2, '17/5'))

    def test_inequality(self):
        self.assertTrue(self.q1 != self.q2)

    def test_eye(self):
        self.assertEqual(Qi.eye(), Qi(0, 1))

    def test_units(self):
        self.assertEqual(Qi.units(), [Qi('1', '0'), Qi('-1', '0'), Qi('0', '1'), Qi('0', '-1')])

    def test_associates(self):
        self.assertEqual(self.q2.associates(), [Qi('-1/2', '-3/5'), Qi('-3/5', '1/2'), Qi('3/5', '-1/2')])

    def test_is_associate(self):
        self.assertTrue(self.q2.is_associate(Qi('-1/2', '-3/5')))
        self.assertFalse(self.q2.is_associate(self.q1))

    # def test_abs(self):
    #     assert False

    # def test_round(self):
    #     assert False

    # def test_floor(self):
    #     assert False

    # def test_ceil(self):
    #     assert False

    def test_random(self):
        seed(7)
        self.assertEqual(Qi.random(), Qi('-2042/3219', '-550/3219'))
