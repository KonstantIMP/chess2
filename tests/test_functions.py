"""
Тестирование пакета utils
"""
import unittest
from chess2.utils.functions import flatten


class UtilsTest(unittest.TestCase):
    def test_flatten(self):
        self.assertEqual(
            flatten([[0, 1], [2], [4, 5]]),
            [0, 1, 2, 4, 5]
        )

        