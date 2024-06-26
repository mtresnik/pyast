import math
from numbers import Number

from pyast.constant import Constant
from pyast.operation import *


class Multiplication(Operation):
    def __init__(self, values):
        if len(values) > 0:
            if isinstance(values[0], Number):
                new_values = list(map(lambda x: Constant(x), values))
                values = new_values
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
        ret = 1
        for elem in self.values:
            ret *= elem.to_number()
        return ret

    def to_string(self):
        return " * ".join(map(str, self.values))

    def evaluate(self, one, other):
        if self == one:
            return other
        return Multiplication(evaluate_values(self, one, other))
