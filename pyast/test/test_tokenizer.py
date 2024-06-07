import unittest

from pyast.parser.tokens.tokenizer import tokenize


class TestTokenizer(unittest.TestCase):

    def test_tokenizer(self):
        token_list = tokenize("123.4 + 6(xyz) + 2.5")
        print("test_tokenizer", ",".join(map(str, token_list)))

    def test_tokenizer_comma_separated(self):
        token_list = tokenize("123.4 + sin(xyz,2x) + 2.5")
        print("test_tokenizer_comma_separated", ",".join(map(str, token_list)))


if __name__ == '__main__':
    unittest.main()
