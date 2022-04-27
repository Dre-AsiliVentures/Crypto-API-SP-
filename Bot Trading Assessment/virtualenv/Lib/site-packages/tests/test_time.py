from unittest import TestCase
from pyutility import limit_time, timeit

from .func import time, error, return_check


class TimeitTest(TestCase):

    def test_timeit1(self):
        v = timeit(time, args=(5,))
        self.assertIsInstance(v, float)

    def test_timeit2(self):
        self.assertRaises(Exception, timeit, error, 5)


class LimitTimeTest(TestCase):

    def test_limit_time_1(self):
        v = limit_time(time, time=2, args=(10,))
        self.assertEqual(v, 55)

    def test_limit_time_2(self):
        self.assertRaises(
            Exception,
            limit_time,
            error,
            time=2,
            args=(2,)
        )

    def test_limit_time_3(self):
        self.assertRaises(
            TimeoutError,
            limit_time,
            time,
            time=2,
            args=(50,)
        )

    def test_limit_time_4(self):
        v = limit_time(
            return_check,
            time=2,
            args=(1, 2, 3),
            kwargs={"four": 4, "five": 5}
        )

        self.assertEqual(v, [1, 2, 3, 4, 5])
