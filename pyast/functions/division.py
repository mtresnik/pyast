import math

from pyast.operation import Operation


class Division(Operation):

    def __init__(self, numerator, denominator):
        super().__init__(*[numerator, denominator])
        self.numerator = numerator
        self.denominator = denominator

    def is_constant(self):
        if self.numerator.is_constant() and self.denominator.is_constant():
            return True
        if self.numerator == self.denominator:
            return True
        return False

    def to_number(self):
        if self.numerator == self.denominator:
            return complex(1, 0)
        if not self.is_constant():
            return complex(math.nan, math.nan)
        numerator = self.numerator.to_number()
        denominator = self.denominator.to_number()
        if numerator == 0 and denominator == 0:
            return complex(math.nan, math.nan)
        if denominator == 0:
            return complex(math.inf, math.inf)
        return self.numerator.to_number() / self.denominator.to_number()

    def to_string(self):
        return "".join([str(self.numerator), "/", str(self.denominator)])

    def evaluate(self, one, other):
        if self == one:
            return other
        return Division(numerator=self.numerator.evaluate(one, other),
                        denominator=self.denominator.evaluate(one, other))
