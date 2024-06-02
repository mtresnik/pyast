import math

from pyast.operation import *


class Addition(Operation):

    def __init__(self, values):
        super().__init__(*values)

    def is_constant(self):
        if len(self.values) == 0:
            return True
        if len(self.values) == 1:
            return self.values[0].is_constant()
        return all_constants(self)

    def to_number(self):
        if not self.is_constant():
            return complex(math.nan, math.nan)
        sum(list(map(lambda op: op.to_number(), self.values)))

    def to_string(self):
        return " + ".join(map(str, self.values))

    def evaluate(self, one, other):
        if self == one:
            return other
        return Addition(evaluate_values(self, one, other))
