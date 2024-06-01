import unittest

from pyast.constant import Constant


class TestComplexArg(unittest.TestCase):

    def test_complex_arg(self):
        c = Constant(complex(1, 2))
        print(c)
        d = 1 + 2j
        print(d)


if __name__ == '__main__':
    unittest.main()
