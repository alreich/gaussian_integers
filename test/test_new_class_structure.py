from unittest import TestCase
from NEW_cayley_dickson_alg import Zi
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
