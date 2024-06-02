import unittest

from pyast.constant import Constant


class TestComplexArg(unittest.TestCase):

    def test_complex_arg(self):
        c = Constant(complex(1, 2))
        print("test_complex_arg", c)

    def test_real_arg(self):
        c = Constant(5.0)
        print("test_real_arg", c)


if __name__ == '__main__':
    unittest.main()
