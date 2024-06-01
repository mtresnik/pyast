import math
import numbers

from pyast import Operation


class Constant(Operation):
    def __init__(self, representation, string_representation=None):
        super().__init__([])
        if isinstance(representation, numbers.Complex):
            self.representation = representation
        else:
            self.representation = complex(math.nan, math.nan)
        self.string_representation = string_representation

    def is_constant(self):
        return True

    def to_number(self):
        return self.representation

    def to_string(self):
        if self.string_representation is not None:
            return self.string_representation
        return str(self.representation)

    def evaluate(self, one, other):
        if self == one:
            return other
        return self


e = Constant(complex(math.e, 0), 'e')

pi = Constant(complex(math.pi, 0), 'π')

TEN = Constant(10)
