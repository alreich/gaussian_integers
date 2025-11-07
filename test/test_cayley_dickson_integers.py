from unittest import TestCase
from cayley_dickson_integers import Zi, SetScalarMult, hypercomplex_string_to_array
from random import seed

class TestZi(TestCase):

    def setUp(self) -> None:
        pass

    def test_constructor_v1(self):
        seed(42)
        self.assertEqual(Zi(0, 0), Zi(0, 0))
        self.assertEqual(Zi(1, 0), Zi(1, 0))
        self.assertEqual(Zi.zero(), Zi(0, 0))
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
        self.assertEqual(str(Zi(Zi(), Zi(1))), 'j')

    def test_constructor_v2(self):
        """Test every possible combination of types that can be used to
        construct a Zi object."""
        #-------------------
        # real type - imag type
        #-------------------

        # float - float
        self.assertEqual(Zi(0.4, 0.85), Zi(0, 1))

        # float - int
        self.assertEqual(Zi(0.4, 7), Zi(0, 7))

        # float - None
        self.assertEqual(Zi(0.4), Zi(0, 0))

        # int - float
        self.assertEqual(Zi(-3, 0.85), Zi(-3, 1))

        # int - int
        self.assertEqual(Zi(-3, 7), Zi(-3, 7))

        # int - None
        self.assertEqual(Zi(-3), Zi(-3, 0))

        # complex - complex
        self.assertEqual(Zi((-1.7+2j), (3-0.75j)), Zi(Zi(-2, 2), Zi(3, -1)))

        # complex - Zi
        self.assertEqual(Zi((-1.7+2j), Zi(-2, 5)), Zi(Zi(-2, 2), Zi(-2, 5)))

        # complex - tuple
        self.assertEqual(Zi((-1.7+2j), (5, -8)), Zi(Zi(-2, 2), Zi(5, -8)))

        # complex - list
        self.assertEqual(Zi((-1.7+2j), [-1, 2]), Zi(Zi(-2, 2), Zi(-1, 2)))

        # complex - None
        self.assertEqual(Zi((-1.7+2j)), Zi(-2, 2))

        # Zi - complex
        self.assertEqual(Zi(Zi(3, -7), (3-0.75j)), Zi(Zi(3, -7), Zi(3, -1)))

        # Zi - Zi
        self.assertEqual(Zi(Zi(3, -7), Zi(-2, 5)), Zi(Zi(3, -7), Zi(-2, 5)))

        # Zi - tuple
        self.assertEqual(Zi(Zi(3, -7), (5, -8)), Zi(Zi(3, -7), Zi(5, -8)))

        # Zi - list
        self.assertEqual(Zi(Zi(3, -7), [-1, 2]), Zi(Zi(3, -7), Zi(-1, 2)))

        # Zi - None
        self.assertEqual(Zi(Zi(3, -7)), Zi(3, -7))

        # tuple - complex
        self.assertEqual(Zi((9, 4), (3-0.75j)), Zi(Zi(9, 4), Zi(3, -1)))

        # tuple - Zi
        self.assertEqual(Zi((9, 4), Zi(-2, 5)), Zi(Zi(9, 4), Zi(-2, 5)))

        # tuple - tuple
        self.assertEqual(Zi((9, 4), (5, -8)), Zi(Zi(9, 4), Zi(5, -8)))

        # tuple - list
        self.assertEqual(Zi((9, 4), [-1, 2]), Zi(Zi(9, 4), Zi(-1, 2)))

        # tuple - None
        self.assertEqual(Zi((9, 4)), Zi(9, 4))

        # list - complex
        self.assertEqual(Zi([-6, 1], (3-0.75j)), Zi(Zi(-6, 1), Zi(3, -1)))

        # list - Zi
        self.assertEqual(Zi([-6, 1], Zi(-2, 5)), Zi(Zi(-6, 1), Zi(-2, 5)))

        # list - tuple
        self.assertEqual(Zi([-6, 1], (5, -8)), Zi(Zi(-6, 1), Zi(5, -8)))

        # list - list
        self.assertEqual(Zi([-6, 1], [-1, 2]), Zi(Zi(-6, 1), Zi(-1, 2)))

        # list - None
        self.assertEqual(Zi([-6, 1]), Zi(-6, 1))

        # None - None
        self.assertEqual(Zi(), Zi(0, 0))

    def test_random(self):
        seed(42)
        n = 4
        size = 10
        zs = [Zi.random(size) for _ in range(n)]
        self.assertEqual(zs, [Zi(10, -7), Zi(-10, -2), Zi(-3, -3), Zi(-6, -7)])

    def test_properties(self):
        z1 = Zi(10, -7)
        self.assertEqual(str(z1), '10-7i')
        self.assertEqual(-z1, Zi(-10, 7))
        self.assertEqual(z1.real, 10)
        self.assertEqual(z1.imag, -7)
        self.assertEqual(z1.conjugate(), Zi(10, 7))
        self.assertEqual(z1.norm, 149)
        self.assertEqual(z1.order, 1)
        self.assertEqual(z1.is_complex, True)
        self.assertEqual(z1.is_quaternion, False)
        self.assertEqual(z1.is_octonion, False)
        self.assertEqual(complex(z1), (10 - 7j))

    def test_quaternion(self):
        z1 = Zi(10, -7); z2 = Zi(-10, -2)
        z3 = Zi(-3, -3); z4 = Zi(-6, -7)
        q1 = Zi(z1, z2)
        q2 = Zi(z3, z4)
        self.assertEqual(q1, Zi(Zi(10, -7), Zi(-10, -2)))
        self.assertEqual(q2, Zi(Zi(-3, -3), Zi(-6, -7)))
        self.assertEqual(q1.order, 2)
        self.assertEqual(q1.is_complex, False)
        self.assertEqual(q1.is_quaternion, True)
        self.assertEqual(q1.norm, 253)
        self.assertEqual(q1.to_array(), [[10, -7], [-10, -2]])
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
        # Zi.scalar_mult(False)  # ==> increase_order first, instead of scalar mult
        with SetScalarMult(False):
            self.assertEqual(q1 * 2, Zi(Zi(20, -14), Zi(-20, -4)))
            self.assertEqual(2 * q1, Zi(Zi(20, -14), Zi(-20, -4)))
        self.assertFalse(Zi.scalar_mult())

    def test_octonion(self):
        q1 = Zi(Zi(10, -7), Zi(-10, -2))
        q2 = Zi(Zi(-3, -3), Zi(-6, -7))
        o0 = Zi(q1, q2)
        self.assertEqual(o0, Zi(Zi(Zi(10, -7), Zi(-10, -2)), Zi(Zi(-3, -3), Zi(-6, -7))))
        self.assertEqual(str(o0), '10-7i-10j-2k-3L-3I-6J-7K')
        self.assertEqual(o0.order, 3)
        self.assertEqual(o0.norm, 356)
        self.assertEqual(o0.is_quaternion, False)
        self.assertEqual(o0.is_octonion, True)

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
        self.assertEqual(str(o1), '7-8i+8j+3k-9L-10I-8J-4K')

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
        self.assertEqual(str(Zi()), '0')
        self.assertEqual(str(Zi(1)), '1')
        self.assertEqual(str(quat), 'j')

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

    def test_parse_hypercomplex_string(self):
        self.assertEqual(hypercomplex_string_to_array('1+2i+3j+4k'), [1, 2, 3, 4])
        self.assertEqual(hypercomplex_string_to_array('-1+3i-3j+7k'), [-1, 3, -3, 7])
        self.assertEqual(hypercomplex_string_to_array('-1-4i-9j-2k'), [-1, -4, -9, -2])
        self.assertEqual(hypercomplex_string_to_array('17-16i-15j-14k'), [17, -16, -15, -14])
        self.assertEqual(hypercomplex_string_to_array('7+2i'), [7, 2])
        self.assertEqual(hypercomplex_string_to_array('7+2j'), [7, 0, 2, 0])
        self.assertEqual(hypercomplex_string_to_array('2i-6k'), [0, 2, 0, -6])
        self.assertEqual(hypercomplex_string_to_array('1-5j+2k'), [1, 0, -5, 2])
        self.assertEqual(hypercomplex_string_to_array('1-5j'), [1, 0, -5, 0])
        self.assertEqual(hypercomplex_string_to_array('3+4i-9k'), [3, 4, 0, -9])
        self.assertEqual(hypercomplex_string_to_array('42i+j-k'), [0, 42, 1, -1])
        self.assertEqual(hypercomplex_string_to_array('6-2i+j-3k'), [6, -2, 1, -3])
        self.assertEqual(hypercomplex_string_to_array('1+i+j+k'), [1, 1, 1, 1])
        self.assertEqual(hypercomplex_string_to_array('-1-i-j-k'), [-1, -1, -1, -1])
        self.assertEqual(hypercomplex_string_to_array('16k-20j+2i-7'), [-7, 2, -20, 16])
        self.assertEqual(hypercomplex_string_to_array('i+4k-3j+2'), [2, 1, -3, 4])
        self.assertEqual(hypercomplex_string_to_array('5k-2i+9+3j'), [9, -2, 3, 5])
        self.assertEqual(hypercomplex_string_to_array('5k-2j+3'), [3, 0, -2, 5])
        self.assertEqual(hypercomplex_string_to_array('1.75-1.75i-1.75j-1.75k'), [1.75, -1.75, -1.75, -1.75])
        self.assertEqual(hypercomplex_string_to_array('2.0j-3k+0.47i-13'), [-13, 0.47, 2.0, -3])
        self.assertEqual(hypercomplex_string_to_array('5.6-3i'), [5.6, -3])
        self.assertEqual(hypercomplex_string_to_array('k-7.6i'), [0, -7.6, 0, 1])
        self.assertEqual(hypercomplex_string_to_array('0'), [0, 0])
        self.assertEqual(hypercomplex_string_to_array('0j+0k'), [0, 0])
        self.assertEqual(hypercomplex_string_to_array('-0j'), [0, 0])
        self.assertEqual(hypercomplex_string_to_array('1-0k'), [1, 0])
        self.assertEqual(hypercomplex_string_to_array('1+2i+3j+4k'), [1, 2, 3, 4])
        self.assertEqual(hypercomplex_string_to_array('7.1E-2 +4.3k+i'), [0.071, 1, 0, 4.3])
        self.assertEqual(hypercomplex_string_to_array('3 - 2E-3i-4j'), [3, -0.002, -4, 0])
        self.assertEqual(hypercomplex_string_to_array('1+2i+3j+4k+5L+6I+7J+8K'), [1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(hypercomplex_string_to_array('2i+3j+4k-1.07+6I+7J+8K'), [-1.07, 2, 3, 4, 0, 6, 7, 8])
        self.assertEqual(hypercomplex_string_to_array('  -1 +3j + 4k+5L +8K - 7J   '), [-1, 0, 3, 4, 5, 0, -7, 8])
        self.assertEqual(hypercomplex_string_to_array('-5L+8K'), [0, 0, 0, 0, -5, 0, 0, 8])
        self.assertEqual(hypercomplex_string_to_array('8.743e-37K'), [0, 0, 0, 0, 0, 0, 0, 8.743e-37])
        self.assertEqual(hypercomplex_string_to_array('1+2i'), [1, 2])
        self.assertEqual(hypercomplex_string_to_array('1+2i-3j-4k'), [1, 2, -3, -4])
        self.assertEqual(hypercomplex_string_to_array('1+2i-3j-4k-5L+6I-7J+8K'), [1, 2, -3, -4, -5, 6, -7, 8])
        self.assertEqual(hypercomplex_string_to_array('1-3k'), [1, 0, 0, -3])
        self.assertEqual(hypercomplex_string_to_array('2i-4k'), [0, 2, 0, -4])
        self.assertEqual(hypercomplex_string_to_array('2j-8K'), [0, 0, 2, 0, 0, 0, 0, -8])
        self.assertEqual(hypercomplex_string_to_array('i+j-k'), [0, 1, 1, -1])
        self.assertEqual(hypercomplex_string_to_array('j+L'), [0, 0, 1, 0, 1, 0, 0, 0])
        self.assertEqual(hypercomplex_string_to_array('2i-1+3k-4j'), [-1, 2, -4, 3])
        self.assertEqual(hypercomplex_string_to_array('L-k'), [0, 0, 0, -1, 1, 0, 0, 0])
        self.assertEqual(hypercomplex_string_to_array('7-2.4e-3i+3.75j-4.0k'), [7, -2.4e-3, 3.75, -4.0])