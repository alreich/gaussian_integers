from unittest import TestCase
from cayley_dickson_integers import Zi, SetScalarMult
from random import seed

class TestZi(TestCase):

    def setUp(self) -> None:
        self.c1 = Zi(4, 5)
        self.c1_conj = Zi(4, -5)
        self.c2 = Zi(1, -2)
        self.c1_x_c2 = Zi(14, -3)  # c1 * c2
        self.c4 = Zi(4, 12)

    def test_constructor(self):
        seed(42)
        # self.assertEqual(Zi(), Zi(77777777, 77777777))
        self.assertEqual(Zi(0, 0), Zi(0, 0))
        self.assertEqual(Zi(1, 0), Zi(1, 0))
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

        self.assertEqual(Zi.zero(), Zi(0, 0))
        self.assertEqual(Zi.zero(1), Zi(0, 0))
        self.assertEqual(Zi.zero(2), Zi(Zi(0, 0), Zi(0, 0)))
        self.assertEqual(Zi.zero(3), Zi(Zi(Zi(0, 0), Zi(0, 0)), Zi(Zi(0, 0), Zi(0, 0))))
        self.assertEqual(Zi.one(), Zi(1, 0))
        self.assertEqual(Zi.one(1), Zi(1, 0))
        self.assertEqual(Zi.one(2), Zi(Zi(1, 0), Zi(0, 0)))
        self.assertEqual(Zi.one(3), Zi(Zi(Zi(1, 0), Zi(0, 0)), Zi(Zi(0, 0), Zi(0, 0))))

        self.assertEqual(Zi((3 + 4j), (1 + 2j)), Zi(Zi(3, 4), Zi(1, 2)))
        self.assertEqual(Zi(Zi(Zi(0), Zi(1)), Zi(Zi(3, 4), Zi(1, 2))),
                         Zi(Zi(Zi(0, 0), Zi(1, 0)), Zi(Zi(3, 4), Zi(1, 2))))
        self.assertEqual(Zi(Zi(Zi(0), Zi(1)), Zi(Zi(3, 4), (1 + 2j))),
                         Zi(Zi(Zi(0, 0), Zi(1, 0)), Zi(Zi(3, 4), Zi(1, 2))))
        self.assertEqual(Zi((1.9 + 2.1j)), Zi(2, 2))
        self.assertEqual(Zi((-1j)), Zi(0, -1))
        self.assertEqual(Zi(Zi(), Zi(1)), Zi(Zi(0, 0), Zi(1, 0)))
        self.assertEqual(str(Zi(Zi(), Zi(1))), '(+1j)')

    def test_random(self):
        seed(42)
        n = 4
        size = 10
        zs = [Zi.random(size) for _ in range(n)]
        self.assertEqual(zs, [Zi(10, -7), Zi(-10, -2), Zi(-3, -3), Zi(-6, -7)])

    def test_properties(self):
        z1 = Zi(10, -7)
        self.assertEqual(str(z1), '(10-7j)')
        self.assertEqual(-z1, Zi(-10, 7))
        self.assertEqual(z1.real, 10)
        self.assertEqual(z1.imag, -7)
        self.assertEqual(z1.conjugate(), Zi(10, 7))
        self.assertEqual(z1.norm, 149)
        self.assertEqual(z1.order(), 1)
        self.assertEqual(z1.is_complex(), True)
        self.assertEqual(z1.is_quaternion(), False)
        self.assertEqual(complex(z1), (10 - 7j))

    def test_quaternion(self):
        z1 = Zi(10, -7); z2 = Zi(-10, -2)
        z3 = Zi(-3, -3); z4 = Zi(-6, -7)
        q1 = Zi(z1, z2)
        q2 = Zi(z3, z4)
        self.assertEqual(q1, Zi(Zi(10, -7), Zi(-10, -2)))
        self.assertEqual(q2, Zi(Zi(-3, -3), Zi(-6, -7)))
        self.assertEqual(q1.order(), 2)
        self.assertEqual(q1.is_complex(), False)
        self.assertEqual(q1.is_quaternion(), True)
        self.assertEqual(q1.norm, 253)
        self.assertEqual(q1 + q2, Zi(Zi(7, -10), Zi(-16, -9)))
        self.assertEqual(q1 - q2, Zi(Zi(13, -4), Zi(-4, 5)))
        self.assertEqual(q1 * q2, Zi(Zi(-125, 49), Zi(-73, -52)))
        self.assertEqual(q1.hamilton_product(q2), q1 * q2)
        self.assertEqual(q2.hamilton_product(q1), q2 * q1)
        # Mult by a real number. Scalar_mult setting shouldn't matter.
        self.assertFalse(Zi.scalar_mult())
        with SetScalarMult(True):
            self.assertEqual(q1 * 2, Zi(Zi(20, -14), Zi(-20, -4)))
            self.assertEqual(2 * q1, Zi(Zi(20, -14), Zi(-20, -4)))
        # Zi.scalar_mult(False)  # ==> Cast first, instead of scalar mult
        with SetScalarMult(False):
            self.assertEqual(q1 * 2, Zi(Zi(20, -14), Zi(-20, -4)))
            self.assertEqual(2 * q1, Zi(Zi(20, -14), Zi(-20, -4)))
        self.assertFalse(Zi.scalar_mult())

    def test_octonion(self):
        q1 = Zi(Zi(10, -7), Zi(-10, -2))
        q2 = Zi(Zi(-3, -3), Zi(-6, -7))
        o0 = Zi(q1, q2)
        self.assertEqual(o0, Zi(Zi(Zi(10, -7), Zi(-10, -2)), Zi(Zi(-3, -3), Zi(-6, -7))))
        self.assertEqual(str(o0), '((10-7i-10j-2k), (-3-3i-6j-7k))')
        self.assertEqual(o0.order(), 3)
        self.assertEqual(o0.norm, 356)
        self.assertEqual(o0.is_quaternion(), False)
        self.assertEqual(o0.is_octonion(), True)

        o1 = Zi(Zi(Zi(10, -7), Zi(-10, -2)), Zi(Zi(-3, -3), Zi(-6, -7)))
        o2 = Zi(Zi(Zi(-3, 6), Zi(9, -10)), Zi(Zi(7, -4), Zi(10, 7)))
        # o3 = Zi(Zi(Zi(3, -3), Zi(4, 8)), Zi(Zi(-2, -10), Zi(-5, 3)))
        self.assertEqual(o1 + o2, Zi(Zi(Zi(7, -1), Zi(-1, -12)), Zi(Zi(4, -7), Zi(4, 0))))
        self.assertEqual(o1 - o2, Zi(Zi(Zi(13, -13), Zi(-19, 8)), Zi(Zi(-10, 1), Zi(-16, -14))))
        self.assertEqual(o1 * o2, Zi(Zi(Zi(200, 204), Zi(1, -15)), Zi(Zi(163, -135), Zi(90, 148))))
        self.assertEqual(o1 + 2, Zi(Zi(Zi(12, -7), Zi(-10, -2)), Zi(Zi(-3, -3), Zi(-6, -7))))
        self.assertEqual(2 + o1, Zi(Zi(Zi(12, -7), Zi(-10, -2)), Zi(Zi(-3, -3), Zi(-6, -7))))
        self.assertEqual(o1 - 2, Zi(Zi(Zi(8, -7), Zi(-10, -2)), Zi(Zi(-3, -3), Zi(-6, -7))))
        self.assertEqual(-(2 - o1), Zi(Zi(Zi(8, -7), Zi(-10, -2)), Zi(Zi(-3, -3), Zi(-6, -7))))
        self.assertEqual(o1.to_array(), [[[10, -7], [-10, -2]], [[-3, -3], [-6, -7]]])
        self.assertTrue(Zi.from_array(o1.to_array()) == o1)

    def test_rand_gen_higher_orders(self):
        seed(42)
        self.assertEqual(Zi.random(), Zi(10, -7))
        self.assertEqual(Zi.random(order=1), Zi(-10, -2))
        self.assertEqual(Zi.random(order=2), Zi(Zi(-3, -3), Zi(-6, -7)))
        o1 = Zi.random(order=3)
        self.assertEqual(str(o1), '((7-8i+8j+3k), (-9-10i-8j-4k))')
        # o2 = Zi.random(order=3)
        # o3 = Zi.random(order=3)

    def test_to_from_array(self):
        q1 = Zi(Zi(10, -7), Zi(-10, -2))
        o1 = Zi(Zi(Zi(10, -7), Zi(-10, -2)), Zi(Zi(-3, -3), Zi(-6, -7)))
        q1arr = q1.to_array()
        o1arr = o1.to_array()
        self.assertEqual(q1arr, [[10, -7], [-10, -2]])
        self.assertEqual(o1arr, [[[10, -7], [-10, -2]], [[-3, -3], [-6, -7]]])
        q1x = Zi.from_array(q1arr)
        o1x = Zi.from_array(o1arr)
        self.assertEqual(q1x, q1)
        self.assertEqual(o1x, o1)

    def test_string(self):
        quat = Zi(Zi(), Zi(1))
        self.assertEqual(str(Zi()), '0j')
        self.assertEqual(str(Zi(1)), '(1+0j)')
        self.assertEqual(str(quat), '(+1j)')
        # self.assertEqual(, )

    def test_add(self):  # __add__ & __radd__
        self.assertEqual(Zi(4, 5) + Zi(1, -2), Zi(5, 3))
        self.assertEqual(Zi(4, 5) + 2, Zi(6, 5))
        self.assertEqual(2 + Zi(4, 5), Zi(6, 5))
        self.assertEqual(Zi(4, 5) + 1.9, Zi(6, 5))
        self.assertEqual(1.9 + Zi(4, 5), Zi(6, 5))
        self.assertEqual(Zi(4, 5) + (1 - 1j), Zi(5, 4))
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
        self.assertEqual(Zi(4, 5) * 1.49999, Zi(4, 5))  # since Zi(1.49999) = Zi(1, 0)
        self.assertEqual(1.49999 * Zi(4, 5), Zi(4, 5))
        self.assertEqual(Zi(4, 5) * (2 - 1j), Zi(13, 6))
        self.assertEqual((2 - 1j) * Zi(4, 5), Zi(13, 6))
        self.assertEqual(Zi(4, 5) * (1.9 - 1.1j), Zi(13, 6))
        self.assertEqual((1.9 - 1.1j) * Zi(4, 5), Zi(13, 6))
