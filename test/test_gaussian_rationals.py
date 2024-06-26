from unittest import TestCase
from gaussians import Zi, Qi
from fractions import Fraction


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

    # def test_max_denominator(self):
    #     assert False

    # def test_set_max_denominator(self):
    #     assert False

    def test_real(self):
        self.assertEqual(self.q1.real, Fraction(2, 1))

    def test_imag(self):
        self.assertEqual(self.q1.imag, Fraction(17, 5))

    def test_conjugate(self):
        self.assertEqual(self.q1.conjugate, Qi(2, '-17/5'))

    # def test_norm(self):
    #     assert False

    # def test_random(self):
    #     assert False

    # def test_inverse(self):
    #     assert False

    # def test_eye(self):
    #     assert False

    # def test_units(self):
    #     assert False

    # def test_associates(self):
    #     assert False

    # def test_is_associate(self):
    #     assert False
