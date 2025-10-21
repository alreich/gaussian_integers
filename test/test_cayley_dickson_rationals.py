from unittest import TestCase
from fractions import Fraction
from cayley_dickson_integers import Zi
from cayley_dickson_rationals import Qi
from random import seed

class TestQi(TestCase):

    def setUp(self) -> None:
        seed(42)

    def test_constructor(self):
        #-------------------
        # re type - im type
        #-------------------

        # str - str
        self.assertEqual(Qi('1/2', '3/4'), Qi(1/2, 3/4))

        # str - float
        self.assertEqual(Qi('1/2', 0.75), Qi(1/2, 3/4))

        # str - int
        self.assertEqual(Qi('1/2', 7), Qi(1/2, 7))

        # str - Fraction
        self.assertEqual(Qi('1/2', Fraction(3, 8)), Qi(1/2, 3/8))

        # str - None
        self.assertEqual(Qi('1/2'), Qi(1/2, 0))

        # float - str
        self.assertEqual(Qi(0.5, '3/4'), Qi(1/2, 3/4))

        # float - float
        self.assertEqual(Qi(0.5, 0.75), Qi(1/2, 3/4))

        # float - int
        self.assertEqual(Qi(0.5, 7), Qi(1/2, 7))

        # float - Fraction
        self.assertEqual(Qi(0.5, Fraction(3, 8)), Qi(1/2, 3/8))

        # float - None
        self.assertEqual(Qi(0.5), Qi(1/2, 0))

        # int - str
        self.assertEqual(Qi(-3, '3/4'), Qi(-3, 3/4))

        # int - float
        self.assertEqual(Qi(-3, 0.75), Qi(-3, 3/4))

        # int - int
        self.assertEqual(Qi(-3, 7), Qi(-3, 7))

        # int - Fraction
        self.assertEqual(Qi(-3, Fraction(3, 8)), Qi(-3, 3/8))

        # int - None
        self.assertEqual(Qi(-3), Qi(-3, 0))

        # Fraction - str
        self.assertEqual(Qi(Fraction(1, 2), '3/4'), Qi(1/2, 3/4))

        # Fraction - float
        self.assertEqual(Qi(Fraction(1, 2), 0.75), Qi(1/2, 3/4))

        # Fraction - int
        self.assertEqual(Qi(Fraction(1, 2), 7), Qi(1/2, 7))

        # Fraction - Fraction
        self.assertEqual(Qi(Fraction(1, 2), Fraction(3, 8)), Qi(1/2, 3/8))

        # Fraction - None
        self.assertEqual(Qi(Fraction(1, 2)), Qi(1/2, 0))

        # complex - complex
        self.assertEqual(Qi((-1.5+2j), (3-0.75j)), Qi(-3/2, 2))

        # complex - Qi
        self.assertEqual(Qi((-1.5+2j), Qi(1/4, 3/4)), Qi(-3/2, 2))

        # complex - Zi
        self.assertEqual(Qi((-1.5+2j), Zi(-2, 5)), Qi(-3/2, 2))

        # TODO: Implement this case
        # Qi - complex
        # <<< NOT IMPLEMENTED YET >>> Qi(1/2, 3/4) is not a supported type

        # TODO: Implement this case
        # Qi - Qi
        # <<< NOT IMPLEMENTED YET >>> Qi(1/2, 3/4) is not a supported type

        # TODO: Implement this case
        # Qi - Zi
        # <<< NOT IMPLEMENTED YET >>> Qi(1/2, 3/4) is not a supported type

        # Zi - complex
        self.assertEqual(Qi(Zi(3, -7), (3-0.75j)), Qi(3, -7))

        # Zi - Qi
        self.assertEqual(Qi(Zi(3, -7), Qi(1/4, 3/4)), Qi(3, -7))

        # Zi - Zi
        self.assertEqual(Qi(Zi(3, -7), Zi(-2, 5)), Qi(3, -7))

# END OF FILE
