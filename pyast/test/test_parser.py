import unittest

from pyast.parser import parse_operation


class TestParser(unittest.TestCase):

    def test_parser_constant(self):
        operation = parse_operation("123")
        print("test_parser_constant", str(operation))

    def test_parser_variable(self):
        operation = parse_operation("abc")
        print("test_parser_variable", str(operation))

    def test_parser_function(self):
        operation = parse_operation("sin(x)")
        print("test_parser_function", str(operation))

    def test_parser_addition(self):
        operation = parse_operation("123 + abc")
        print("test_parser_addition", str(operation))

    def test_parser_multiplication(self):
        operation = parse_operation("a * b * c + iabei")
        print("test_parser_multiplication", str(operation))

    def test_parser_functions_of_functions(self):
        operation = parse_operation("sin(log_(x,y))")
        print("test_parser_functions_of_functions", str(operation))

    def test_parentheses(self):
        operation = parse_operation("(123 + 2i + (2x))")
        print("test_parentheses", str(operation))


if __name__ == '__main__':
    unittest.main()
