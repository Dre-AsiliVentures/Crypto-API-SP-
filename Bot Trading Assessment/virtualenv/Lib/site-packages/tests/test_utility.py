from unittest import TestCase
from pyutility import limit_resource, measureit

from .func import memory, time, return_check, error


class MeasureitTest(TestCase):

    def test_measureit_1(self):
        v = measureit(memory, args=(100,))
        self.assertIsInstance(v, tuple)

    def test_measureit_2(self):
        v = measureit(time, args=(15,))
        self.assertIsInstance(v[0], int)
        self.assertIsInstance(v[1], float)

    def test_measureit_3(self):
        v = measureit(time, args=(15,))
        self.assertIsInstance(v, tuple)

    def test_measureit_4(self):
        self.assertRaises(Exception, measureit, error, 100)


class LimitResourceTest(TestCase):

    def test_limit_resource_1(self):
        v = limit_resource(memory, time=2, args=(300,))
        self.assertEqual(v, -1)

    def test_limit_resource_2(self):
        v = limit_resource(time, time=2, args=(3,))
        self.assertEqual(v, 2)

    def test_limit_resource_3(self):
        self.assertRaises(Exception, error)

    def test_limit_resource_4(self):
        self.assertRaises(
            MemoryError,
            limit_resource,
            memory,
            args=(100_000_000,),
            time=2
        )

    def test_limit_resource_5(self):
        self.assertRaises(
            TimeoutError,
            limit_resource,
            time,
            args=(50,),
            time=2
        )

    def test_limit_resource_6(self):
        v = limit_resource(
            return_check,
            time=2,
            args=(1, 2, 3),
            kwargs={"four": 4, "five": 5}
        )

        self.assertEqual(v, [1, 2, 3, 4, 5])
