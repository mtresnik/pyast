import math

from pyast.operation import Operation


class Power(Operation):

    def __init__(self, base, exponent):
        super().__init__(*[base, exponent])
        self.base = base
        self.exponent = exponent

    def is_constant(self):
        if self.base.is_constant() and self.exponent.is_constant():
            return True
        if self.exponent.is_constant() and self.exponent.to_number() == 0:
            return True
        return False

    def to_number(self):
        if not self.is_constant():
            return complex(math.nan, math.nan)
        if self.exponent.is_constant() and self.exponent.to_number() == 0:
            if self.base.is_constant() and self.base.to_number() == 0:
                return complex(math.nan, math.nan)
            if not self.base.is_constant():
                return 1
        if self.base.is_constant() and self.base.to_number() == 0:
            if (self.exponent.is_constant() and
                    self.exponent.to_number().real() < 0 and
                    self.exponent.to_number().imag() == 0):
                return complex(math.inf, 0)
        return pow(self.base.to_number(), self.exponent.to_number())

    def to_string(self):
        return "".join([str(self.base), " ^ ", str(self.exponent)])

    def evaluate(self, one, other):
        if self == one:
            return other
        return Power(self.base.evaluate(one, other), self.exponent.evaluate(one, other))
