import math

from pyast import Operation


class Variable(Operation):

    def __init__(self, name):
        super(Variable, self).__init__([])
        self.name = name

    def is_constant(self):
        return False

    def to_number(self):
        return complex(math.nan, math.nan)

    def to_string(self):
        return str(self.name)

    def evaluate(self, one, other):
        if self == one:
            return other
        return self
