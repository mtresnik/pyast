import unittest

from pyast.parser import parse


class TestParser(unittest.TestCase):

    def test_parser_constant(self):
        operation = parse("123")
        print("test_parser_constant", str(operation))

    def test_parser_variable(self):
        operation = parse("abc")
        print("test_parser_variable", str(operation))

    def test_parser_function(self):
        operation = parse("sin(x)")
        print("test_parser_function", str(operation))

    def test_parser_addition(self):
        operation = parse("123 + abc")
        print("test_parser_addition", str(operation))


if __name__ == '__main__':
    unittest.main()
