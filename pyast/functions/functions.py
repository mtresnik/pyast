from pyast.constant import *
from pyast.functions import *
from pyast.functions import Multiplication, Sin
from pyast.variable import Variable


class FunctionBuilder:
    def __init__(self, num_params, func):
        self.num_params = num_params
        self.func = func


runtime_functions = {
    "sin": FunctionBuilder(1, lambda values: Sin(values[0])),
    "cos": FunctionBuilder(1, lambda values: Cos(values[0])),
    "tan": FunctionBuilder(1, lambda values: Tan(values[0])),
    "arcsin": FunctionBuilder(1, lambda values: ArcSin(values[0])),
    "arccos": FunctionBuilder(1, lambda values: ArcCos(values[0])),
    "arctan": FunctionBuilder(1, lambda values: ArcTan(values[0])),
    "abs": FunctionBuilder(1, lambda values: Abs(values[0])),
    "log": FunctionBuilder(1, lambda values: Log(TEN, values[0])),
    "ln": FunctionBuilder(1, lambda values: Log(e, values[0])),
    "log_": FunctionBuilder(1, lambda values: Log(values[0], values[1])),
}

reserved = set(runtime_functions.keys())


def add_function(name, num_params, func):
    runtime_functions[name] = FunctionBuilder(num_params, func)
    reserved.add(name)


def build_function(name, params):
    if name in runtime_functions:
        builder = runtime_functions[name]
        if len(params) >= builder.num_params:
            return builder.func(params)
    values = []
    for char in name:
        values.append(Variable(char))
    return Multiplication(values)
