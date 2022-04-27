from unittest import TestCase
from pyutility import limit_memory, memoryit

from .func import memory, error, return_check


class MemoryitTest(TestCase):

    def test_memoryit1(self):
        v = memoryit(memory, args=(5,))
        self.assertIsInstance(v, int)

    def test_memoryit2(self):
        self.assertRaises(Exception, memoryit, error, 5)


class LimitMemoryTest(TestCase):

    def test_limit_memory_1(self):
        v = limit_memory(memory, args=(10,))
        self.assertEqual(v, -1)

    def test_limit_memory_2(self):
        self.assertRaises(
            Exception,
            limit_memory,
            error,
            args=(100_000_000,)
        )

    def test_limit_memory_3(self):
        self.assertRaises(
            MemoryError,
            limit_memory,
            memory,
            args=(500_000_000,)
        )

    def test_limit_memory_4(self):
        v = limit_memory(
            return_check,
            args=(1, 2, 3),
            kwargs={"four": 4, "five": 5}
        )

        self.assertEqual(v, [1, 2, 3, 4, 5])
