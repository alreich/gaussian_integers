from unittest import TestCase
from src.gaussians import Zi, Qi

class TestZi(TestCase):

    def setUp(self) -> None:
        self.c1 = Zi(4, 5)
        self.c1_conj = Zi(4, -5)
        self.c2 = Zi(1, -2)
        self.c1_x_c2 = Zi(14, -3)  # c1 * c2
        self.c4 = Zi(4, 12)

    def test_constructor(self):
        self.assertEqual(Zi(), Zi(0, 0))
        self.assertEqual(Zi(1), Zi(1, 0))
        self.assertEqual(Zi.eye(), Zi(0, 1))
        self.assertEqual(Zi.two(), Zi(1, 1))
        self.assertEqual(Zi(2.3, 3.8), Zi(2, 4))
        self.assertEqual(Zi(-2.3, 3.8), Zi(-2, 4))
        self.assertEqual(Zi(2.3, -3.8), Zi(2, -4))
        self.assertEqual(Zi(-2.3, -3.8), Zi(-2, -4))
        self.assertEqual(Zi(2.3, 4), Zi(2, 4))
        self.assertEqual(Zi(-2.3, 4), Zi(-2, 4))
        self.assertEqual(Zi(2, 3.8), Zi(2, 4))
        self.assertEqual(Zi(2, -3.8), Zi(2, -4))
        self.assertEqual(Zi(2.3), Zi(2, 0))
        self.assertEqual(Zi(2), Zi(2, 0))
        self.assertEqual(Zi((2.3 - 3.7j)), Zi(2, -4))
        self.assertEqual(Zi(-3.3j), Zi(0, -3))

    def test_add(self):  # __add__ & __radd__
        self.assertEqual(Zi(4, 5) + Zi(1, -2), Zi(5, 3))
        self.assertEqual(Zi(4, 5) + 2, Zi(6, 5))
        self.assertEqual(2 + Zi(4, 5), Zi(6, 5))
        self.assertEqual(Zi(4, 5) + 1.9, Zi(6, 5))
        self.assertEqual(1.9 + Zi(4, 5), Zi(6, 5))
        self.assertEqual(Zi(4, 5) + (1-1j), Zi(5, 4))
        self.assertEqual((1 - 1j) + Zi(4, 5), Zi(5, 4))

    def test_sub(self):  # __sub__ & __rsub__
        self.assertEqual(Zi(4, 5) - Zi(1, -2), Zi(3, 7))
        self.assertEqual(Zi(4, 5) - 2, Zi(2, 5))
        self.assertEqual(2 - Zi(4, 5), Zi(-2, -5))
        self.assertEqual(Zi(4, 5) - 1.9, Zi(2, 5))
        self.assertEqual(1.9 - Zi(4, 5), Zi(-2, -5))
        self.assertEqual(Zi(4, 5) - (1 - 1j), Zi(3, 6))
        self.assertEqual((1 - 1j) - Zi(4, 5), Zi(-3, -6))

    def test_mul(self):  # __mul__ & __rmul__
        self.assertEqual(Zi(4, 5) * Zi(1, -2), Zi(14, -3))
        self.assertEqual(Zi(4, 5) * 2, Zi(8, 10))
        self.assertEqual(2 * Zi(4, 5), Zi(8, 10))
        self.assertEqual(Zi(4, 5) * 1.9, Zi(8, 10))
        self.assertEqual(1.9 * Zi(4, 5), Zi(8, 10))
        self.assertEqual(Zi(4, 5) * 1.49999, Zi(4, 5))
        self.assertEqual(1.49999 * Zi(4, 5), Zi(4, 5))
        self.assertEqual(Zi(4, 5) * (2-1j), Zi(13, 6))
        self.assertEqual((2-1j) * Zi(4, 5), Zi(13, 6))
        self.assertEqual(Zi(4, 5) * (1.9-1.1j), Zi(13, 6))
        self.assertEqual((1.9-1.1j) * Zi(4, 5), Zi(13, 6))

    def test_truediv(self):  # __truediv__ & __rtruediv__
        self.assertEqual(Zi(4, 5) / Zi(1, -2), Qi('-6/5', '13/5'))
        self.assertEqual(Zi(4, 5) / Zi(1, -2), Qi('-6/5', '13/5'))
        self.assertEqual(Zi(4, 5) / (1.1 - 1.9j), Qi('-255/241', '655/241'))
        self.assertEqual(Zi(4, 5) / (0.9 - 2.3j), Qi('-79/61', '137/61'))
        self.assertEqual(complex(Zi(4, 5) / (0.9 - 2.3j)), (-1.2950819672131149 + 2.2459016393442623j))
        self.assertEqual(complex(Zi(4, 5)) / (0.9 - 2.3j), (-1.2950819672131149 + 2.2459016393442623j))
        self.assertEqual(Zi(4, 5) / 5, Qi('4/5', '1'))
        self.assertEqual(Zi(4, 8) / 2, Zi(2, 4))
        self.assertEqual(Zi(4, 5) / 5.3, Qi('40/53', '50/53'))
        self.assertEqual((1 - 2j) / Zi(4, 5), Qi('-6/41', '-13/41'))
        self.assertEqual(5.0 / Zi(4, 5), Qi('20/41', '-25/41'))
        self.assertEqual(5 / Zi(4, 5), Qi('20/41', '-25/41'))

    def test_floordiv(self):  # __floordiv__ & __rfloordiv__
        self.assertEqual(self.c1_x_c2 // self.c1, self.c2)
        self.assertEqual(self.c1_x_c2 // self.c2, self.c1)
        self.assertEqual(Zi(4, 12) // 4, Zi(1, 3))

    def test_neg(self):  # __neg__
        self.assertEqual(-Zi(1, -2), Zi(-1, 2))

    def test_pow(self):  # __pow__
        self.assertEqual(self.c1 ** 3, Zi(-236, 115))
        self.assertEqual(self.c1 ** 1, self.c1)
        self.assertEqual(self.c1 ** 0, Zi(1))
        self.assertEqual(self.c1 ** -1, Qi('4/41', '-5/41'))
        self.assertEqual(self.c1 ** -2, Qi('-9/1681', '-40/1681'))
        self.assertEqual(1 / self.c1 ** 2, self.c1 ** -2)

    def test_complex(self):  # __complex__
        self.assertEqual(complex(self.c1), (4+5j))

    def test_str(self):  # __str__
        self.assertEqual(str(self.c1), "(4+5j)")

    def test_repr(self):  # __repr__
        self.assertEqual(repr(self.c1), "Zi(4, 5)")

    def test_equal(self):  # __eq__
        self.assertTrue(self.c1 == Zi(4, 5))
        self.assertFalse(self.c1 == self.c2)

    def test_not_equal(self):  # __ne__
        self.assertTrue(self.c1 != self.c2)

    def test_eye(self):
        self.assertEqual(Zi.eye(), Zi(0, 1))

    def test_units(self):
        self.assertEqual(Zi.units(), [Zi(1, 0), Zi(-1, 0), Zi(0, 1), Zi(0, -1)])

    def test_conj(self):
        self.assertEqual(self.c1.conjugate, self.c1_conj)

    def test_norm(self):
        self.assertEqual(self.c1.norm, 41)

    def test_associates(self):
        self.assertEqual(self.c1.associates(), [Zi(-4, -5), Zi(-5, 4), Zi(5, -4)])

    def test_is_associate(self):
        self.assertTrue(self.c1.is_associate(Zi(-4, -5)))
        self.assertFalse(self.c1.is_associate(self.c2))

    def test_divmod_1(self):
        a = Zi(4, 5)
        b = Zi(1, -2)
        q, r = Zi.modified_divmod(a, b)
        self.assertEqual(a, b * q + r)

    def test_divmod_2(self):
        a = Zi(27, -23)
        b = Zi(8, 1)
        q, r = Zi.modified_divmod(a, b)
        self.assertEqual(a, b * q + r)

    def test_divmod_3(self):
        a = Zi(11, 10)
        b = Zi(4, 1)
        q, r = Zi.modified_divmod(a, b)
        self.assertEqual(a, b * q + r)

    def test_divmod_4(self):
        a = Zi(41, 24)
        b = Zi(11, -2)
        q, r = Zi.modified_divmod(a, b)
        self.assertEqual(a, b * q + r)

    def test_divmod_5(self):
        a = Zi(37, 2)
        b = Zi(11, 2)
        q, r = Zi.modified_divmod(a, b)
        self.assertEqual(a, b * q + r)

    def test_divmod_6(self):
        a = Zi(1, 8)
        b = Zi(2, -4)
        q, r = Zi.modified_divmod(a, b)
        self.assertEqual(a, b * q + r)

    def test_mod_1(self):
        a = Zi(4, 5)
        b = Zi(1, -2)
        self.assertEqual(a % b, -1)

    def test_gcd_1(self):
        alpha = Zi(32, 9)
        beta = Zi(4, 11)
        self.assertEqual(Zi.gcd(alpha, beta), Zi(0, -1))

    def test_gcd_2(self):
        alpha = Zi(32, 9)
        beta = Zi(4, 11)
        self.assertEqual(Zi.gcd(beta, alpha), Zi(0, -1))

    def test_gcd_3(self):
        alpha = Zi(11, 3)
        beta = Zi(1, 8)
        self.assertEqual(Zi.gcd(alpha, beta), Zi(1, -2))
