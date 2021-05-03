import unittest
from datetime import date

from main import Cell, fill_series

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_fill_series(self):
        result = fill_series([
            (date(2021, 3, 1), 1337),
        ])

        expected = [
            Cell(date(2021, 2, 28), 0, True),
            Cell(date(2021, 3,  1), 1337, False),
            Cell(date(2021, 3,  2), 0, True),
            Cell(date(2021, 3,  3), 0, True),
            Cell(date(2021, 3,  4), 0, True),
            Cell(date(2021, 3,  5), 0, True),
            Cell(date(2021, 3,  6), 0, True),
        ]

        self.assertEqual(expected, result)

if __name__ == '__main__':
    unittest.main()
