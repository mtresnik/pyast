import cmath
import math

from pyast.operation import Operation


class Log(Operation):

    def __init__(self, base, inner):
        super().__init__([base, inner])
        self.base = base
        self.inner = inner

    def is_constant(self):
        return self.base.is_constant() and self.inner.is_constant()

    def to_number(self):
        if not self.is_constant():
            return complex(math.nan, math.nan)
        cmath.log(self.inner.to_number(), self.base.to_number())

    def to_string(self):
        return "".join(["log(", str(self.base), ",", str(self.inner), ")"])

    def evaluate(self, one, other):
        if self == one:
            return other
        return Log(self.base.evaluate(one, other), self.inner.evaluate(one, other))
