import random
import unittest
from timeit import default_timer as timer

from pyast import util


class TestContainsAll(unittest.TestCase):

    def test_shuffled_arrays_single_threaded(self):
        input_list = [random.random() for i in range(10000)]
        other_list = []
        other_list.extend(input_list)
        random.shuffle(other_list)
        start = timer()
        util.contains_all(input_list, other_list)
        end = timer()
        print(end - start)


if __name__ == '__main__':
    unittest.main()
