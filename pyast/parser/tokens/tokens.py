number = 0
operator = 1
open_parenthesis = 2
close_parenthesis = 3
text = 4
function = 5
variable = 6

plus = "+"
minus = "-"


class Token:
    def __init__(self, start_index, end_index, token_type, representation=None):
        self.start_index = start_index
        self.end_index = end_index
        self.token_type = token_type
        self.representation = representation

    def convert(self, other_type):
        return Token(self.start_index, self.end_index, other_type, self.representation)

    def __str__(self):
        return f'Token({self.start_index}, {self.end_index}, {self.token_type}, {self.representation})'

    def __eq__(self, other):
        return (self.start_index == other.start_index and
                self.end_index == other.end_index and
                self.token_type == other.token_type and
                self.representation == other.representation)


def single_index(index, token_type):
    return Token(index, index, token_type, None)


def null_index(token_type, representation):
    return Token(-1, -1, token_type, representation)


def index_processed(index, token_list):
    for t in token_list:
        if t.start_index <= index <= t.end_index:
            return True
    return False
