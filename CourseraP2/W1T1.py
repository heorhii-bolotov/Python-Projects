import unittest


def factorize(x):
    """ Factorize positive integer and return its factors.
        :type x: int,>=0
        :rtype: tuple[N],N>0
    """
    pass


class TestFactorize(unittest.TestCase):
    def _factorize(self, n):
        while n > 1:
            for i in range(2, int(n) + 1):
                if n % i == 0:
                    n /= i
                    yield i
                    break

    def test_wrong_types_raise_exception(self):
        for n in ["string", 1.5]:
            with self.subTest(x=n):
                self.assertRaises(TypeError, factorize, n)

    def test_negative(self):
        for n in [-1, -10, -100]:
            with self.subTest(x=n):
                self.assertRaises(ValueError, factorize, n)

    def test_zero_and_one_cases(self):
        for n in [0, 1]:
            with self.subTest(x=n):
                self.assertEqual(factorize(n), (n, ))

    def test_simple_numbers(self):
        for n in [3, 13, 29]:
            with self.subTest(x=n):
                self.assertEqual(factorize(n), (n, ))

    def test_two_simple_multipliers(self):
        for n in [6, 26, 121]:
            with self.subTest(x=n):
                self.assertEqual(factorize(n), tuple([i for i in self._factorize(n)]))

    def test_many_multipliers(self):
        for n in [1001, 9699690]:
            with self.subTest(x=n):
                self.assertEqual(factorize(n), tuple([i for i in self._factorize(n)]))

