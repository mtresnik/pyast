import math

from pyast.operation import Operation, all_constants, evaluate_values


class Subtraction(Operation):
    def __init__(self, values):
        super().__init__(values)

    def is_constant(self):
        if len(self.values) == 0:
            return True
        if len(self.values) == 1:
            return self.values[0].is_constant()
        return all_constants(self)

    def to_number(self):
        if not self.is_constant():
            return complex(math.nan, math.nan)
        if len(self.values) == 0:
            return 0
        ret_value = self.values[0].to_number()
        for i in range(1, len(self.values)):
            ret_value -= self.values[i].to_number()
        return ret_value

    def to_string(self):
        return " - ".join(map(str, self.values))

    def evaluate(self, one, other):
        if self == one:
            return other
        return Subtraction(evaluate_values(self, one, other))
