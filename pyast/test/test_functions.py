import math
import unittest

from pyast.functions import Sin, Cos, Tan


class TestFunctions(unittest.TestCase):

    def test_sin(self):
        sin = Sin(math.pi)
        print("test_sin", sin)

    def test_cos(self):
        cos = Cos(math.pi / 4)
        print("test_cos", cos)

    def test_tan(self):
        tan = Tan(math.pi / 4)
        print("test_tan", tan)


if __name__ == '__main__':
    unittest.main()
