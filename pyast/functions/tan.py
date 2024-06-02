import cmath
import math
import numbers

from pyast.constant import Constant
from pyast.operation import Operation


class Tan(Operation):
    def __init__(self, inner):
        if isinstance(inner, numbers.Complex):
            inner = Constant(inner)
        super().__init__(*[inner])
        self.inner = inner

    def is_constant(self):
        return self.inner.is_constant()

    def to_number(self):
        if not self.is_constant():
            return complex(math.nan, math.nan)
        return cmath.tan(self.inner.to_number())

    def to_string(self):
        return "".join(["tan(", str(self.inner), ")"])

    def evaluate(self, one, other):
        if self == one:
            return other
        return Tan(self.inner.evaluate(one, other))
