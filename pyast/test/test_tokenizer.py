import unittest

from pyast.parser.tokens.tokenizer import tokenize


class TestTokenizer(unittest.TestCase):

    def test_tokenizer(self):
        token_list = tokenize("123.4 + 6(xyz) + 2.5")
        print(",".join(map(str, token_list)))


if __name__ == '__main__':
    unittest.main()
