import unittest

from pyast import *


class TestFunctions(unittest.TestCase):

    def test_functions(self):
        c = Constant(complex(1, 2))
        print(c)
        d = 1 + 2j
        print(d)


if __name__ == '__main__':
    unittest.main()
