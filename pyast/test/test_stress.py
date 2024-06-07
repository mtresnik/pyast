from math import floor
from timeit import default_timer as timer
import unittest

from pyast.parser import parseOperation


class StressTest(unittest.TestCase):

    def test_stress1(self):
        num_iterations = 20
        times = []
        string_size = 200
        input_string = ""
        for i in range(string_size):
            input_string += str(i)
            if i < string_size - 1:
                input_string += " + "
        print(input_string)
        for i in range(num_iterations):
            start = timer()
            operation = parseOperation(input_string)
            end = timer()
            times.append(floor((end - start) * 1000))
        print(times)


if __name__ == '__main__':
    unittest.main()
