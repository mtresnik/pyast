from abc import ABC, abstractmethod

from pyast.util import contains_all


class Operation(ABC):
    def __init__(self, *args):
        self.values = []
        for arg in args:
            if isinstance(arg, Operation):
                self.values.append(arg)

    def get_values(self):
        return self.values

    @abstractmethod
    def is_constant(self):
        pass

    @abstractmethod
    def to_number(self):
        pass

    @abstractmethod
    def to_string(self):
        pass

    @abstractmethod
    def evaluate(self, one, other):
        pass

    def __str__(self):
        if self.is_constant():
            num = self.to_number()
            if num.imag == 0:
                if num.real < 1e-10:
                    num = 0
                return str(num.real)
            return str(num).replace("j", "i")
        return self.to_string()

    def __eq__(self, other):
        if not isinstance(other, Operation):
            return False
        self_constant = self.is_constant()
        other_constant = other.is_constant()
        if self_constant and other_constant:
            return self.to_number() == other.to_number()
        if self_constant and not other_constant:
            return False
        self_values = self.get_values()
        other_values = other.get_values()
        if len(self_values) == 0 and len(other_values) == 0:
            return str(self) == str(other)
        self_type = type(self).__name__
        other_type = type(other).__name__
        self_flattened = deep_flatten(self)
        other_flattened = deep_flatten(other)
        if self_type == other_type and len(self_flattened) != len(other_flattened):
            return False
        if self_type == other_type and contains_all(self_values, other_values):
            return True
        return str(self) == str(other)


def has_nested_values(operation_list):
    for operation in operation_list:
        if isinstance(operation, Operation):
            if len(operation.get_values()) > 0:
                return True
    return False


def flatten(values):
    if len(values) == 0:
        return values
    ret_list = []
    for elem in values:
        child_values = elem.get_values()
        if len(child_values) > 0:
            ret_list.extend(child_values)
        else:
            ret_list.append(elem)
    return ret_list


def deep_flatten(operation):
    if not isinstance(operation, Operation):
        return []
    ret_list = [operation]
    while has_nested_values(ret_list):
        ret_list = flatten(ret_list)
    return ret_list


def all_constants(operation):
    flattened = deep_flatten(operation)
    for elem in flattened:
        if not elem.is_constant():
            return False
    return True


def _map_inner(a, one, other):
    if a == one:
        return other
    return a.evaluate(one, other)


def evaluate_values(a, one, other):
    values = a.get_values()
    return list(map(lambda elem: _map_inner(elem, one, other), values))
