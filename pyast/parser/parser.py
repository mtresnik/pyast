import math
from abc import ABC, abstractmethod

from pyast import variables, constant
from pyast.constant import Constant
from pyast.functions import *
from pyast.parser.tokens import tokenizer, tokens
from pyast.variable import Variable

number = tokens.number
parentheses = tokens.open_parenthesis
function = tokens.function
variable = tokens.variable


def _get_tokens(intermediates):
    ret_list = []
    for op in intermediates:
        ret_list.extend(op.get_tokens())
    return ret_list


class _Intermediate(ABC):
    def __init__(self, start_index, end_index):
        self.start_index = start_index
        self.end_index = end_index

    @abstractmethod
    def get_tokens(self):
        pass

    @abstractmethod
    def compile(self):
        pass

    def __str__(self):
        t = str(type(self))
        return f'[type: {t}, range: [{self.start_index}, {self.end_index}], tokens: {",".join(map(str, self.get_tokens()))}]'

    def __eq__(self, other):
        if self.start_index != other.start_index or self.end_index != other.end_index:
            return False
        return set(self.get_tokens()) == set(other.get_tokens())

    def __hash__(self):
        return hash((self.start_index, self.end_index))


class _INumber(_Intermediate):

    def __init__(self, start_index, end_index, token):
        super().__init__(start_index, end_index)
        self.token = token

    def get_tokens(self):
        return [self.token]

    def compile(self):
        representation = complex(str(self.token.representation.replace("i", "j").replace(" ", "")))
        return Constant(representation)


class _IVariable(_Intermediate):

    def __init__(self, start_index, end_index, token):
        super().__init__(start_index, end_index)
        self.token = token

    def get_tokens(self):
        return [self.token]

    def compile(self):
        return Variable(self.token.representation)


class _IAddition(_Intermediate):

    def __init__(self, start_index, end_index, left, right):
        super().__init__(start_index, end_index)
        self.left = left
        self.right = right

    def get_tokens(self):
        return _get_tokens([self.left, self.right])

    def compile(self):
        return Addition([self.left.compile(), self.right.compile()])


class _ISubtraction(_Intermediate):

    def __init__(self, start_index, end_index, left, right):
        super().__init__(start_index, end_index)
        self.left = left
        self.right = right

    def get_tokens(self):
        return _get_tokens([self.left, self.right])

    def compile(self):
        return Subtraction([self.left.compile(), self.right.compile()])


class _IDivision(_Intermediate):
    def __init__(self, start_index, end_index, left, right):
        super().__init__(start_index, end_index)
        self.left = left
        self.right = right

    def get_tokens(self):
        return _get_tokens([self.left, self.right])

    def compile(self):
        return Division(self.left.compile(), self.right.compile())


class _IIdentity(_Intermediate):

    def __init__(self, start_index, end_index, inner):
        super().__init__(start_index, end_index)
        self.inner = inner

    def get_tokens(self):
        return self.inner.get_tokens()

    def compile(self):
        return self.inner.compile()


class _INegation(_Intermediate):

    def __init__(self, start_index, end_index, inner):
        super().__init__(start_index, end_index)
        self.inner = inner

    def get_tokens(self):
        return self.inner.get_tokens()

    def compile(self):
        return Negation(self.inner.compile())


class _IMultiplication(_Intermediate):
    def __init__(self, start_index, end_index, left, right):
        super().__init__(start_index, end_index)
        self.left = left
        self.right = right

    def get_tokens(self):
        return _get_tokens([self.left, self.right])

    def compile(self):
        return Multiplication([self.left.compile(), self.right.compile()])


class _IParentheses(_Intermediate):
    def __init__(self, start_index, end_index, inner):
        super().__init__(start_index, end_index)
        self.inner = inner

    def get_tokens(self):
        return self.inner.get_tokens()

    def compile(self):
        return Parentheses(self.inner.compile())


class _IPower(_Intermediate):
    def __init__(self, start_index, end_index, left, right):
        super().__init__(start_index, end_index)
        self.left = left
        self.right = right

    def get_tokens(self):
        return _get_tokens([self.left, self.right])

    def compile(self):
        return Power(self.left.compile(), self.right.compile())


class _IFunction(_Intermediate):
    def __init__(self, start_index, end_index, name, inner):
        super().__init__(start_index, end_index)
        self.name = name
        self.inner = inner

    def get_tokens(self):
        return _get_tokens(self.inner)

    def compile(self):
        return build_function(self.name, list(map(lambda x: x.compile(), self.inner)))


def _validate_string(input_string):
    balance = 0
    for char in input_string:
        if char == '(':
            balance += 1
        elif char == ')':
            balance -= 1
    if balance != 0:
        raise ValueError("Invalid string: unbalanced parentheses")
    accumulate = ""
    for char in input_string:
        if str(char) == tokenizer.decimal and tokenizer.decimal in accumulate:
            raise ValueError("Invalid string: multiple decimal points in a number")
        if char not in tokenizer.valid_numbers:
            accumulate = ""
        else:
            accumulate += char


def _validate_syntax(token_list):
    for curr, next_token in zip(token_list, token_list[1:]):
        if curr.token_type == tokens.operator:
            if curr.representation == "+" or curr.representation == "-":
                if next_token.token_type == tokens.operator or next_token.token_type == tokens.close_parenthesis:
                    raise ValueError("Invalid string: consecutive operators or operator at the end of the expression")


class TokenSet:
    def __init__(self, start_index, end_index, token_set_type, token_list, representation):
        self.start_index = start_index
        self.end_index = end_index
        self.token_set_type = token_set_type
        self.token_list = token_list
        self.representation = representation

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.start_index == other.start_index and \
                self.end_index == other.end_index and \
                self.token_set_type == other.token_set_type and \
                self.representation == other.representation and \
                set(self.token_list) == set(other.token_list)
        return False

    def __str__(self):
        return f'TokenSet(start_index={self.start_index}, end_index={self.end_index}, token_set_type={self.token_set_type}, token_list={self.token_list}, representation={self.representation})'


def _generate_parentheses(input_list):
    ret_list = []
    inner = []
    balance = 0
    start_index = -1
    for i, token in enumerate(input_list):
        if token.token_type == tokens.open_parenthesis:
            balance -= 1
        elif token.token_type == tokens.close_parenthesis:
            balance += 1
        if balance == -1 and token.token_type == tokens.open_parenthesis:
            start_index = i
        if balance == 0 and token.token_type == tokens.close_parenthesis:
            j = start_index + 1
            while j < i:
                inner.append(input_list[j])
                j += 1
            ret_list.append(TokenSet(start_index, j, parentheses, inner, None))
            start_index = -1
            inner = []
    return ret_list


def _index_processed_token(i, token_list):
    for token in token_list:
        if token.start_index <= i <= token.end_index:
            return True
    return False


def _generate_functions(current, input_list):
    clone = []
    clone.extend(current)
    ret_list = []
    ret_list.extend(current)
    for i, token in enumerate(input_list):
        if not _index_processed_token(i, current):
            if token.token_type == tokens.function:
                found = None
                found_index = -1
                expected_index = i + 1
                for j, set in enumerate(clone):
                    if set.token_set_type == parentheses:
                        if set.start_index == expected_index:
                            found = set
                            found_index = j
                            break
                if found is None:
                    raise ValueError(f"could not find parentheses for given function {str(token.representation)}")
                clone.pop(found_index)
                found_index = ret_list.index(found)
                ret_list.pop(found_index)
                ret_list.append(TokenSet(i, found.end_index, function, found.token_list, token.representation))
    return ret_list


def _generate_variables(current, input_list):
    ret_list = current
    for i, token in enumerate(input_list):
        if not _index_processed_token(i, current):
            if token.token_type == tokens.variable:
                ret_list.append(TokenSet(i, i, variable, [token], token.representation))
    ret_list.sort(key=lambda x: x.start_index)
    return ret_list


def _generate_numbers(current, input_list):
    ret_list = []
    ret_list.extend(current)
    for i, token in enumerate(input_list):
        if not _index_processed_token(i, current):
            if token.token_type == tokens.number:
                ret_list.append(TokenSet(i, i, number, [token], None))
    ret_list.sort(key=lambda x: x.start_index)
    return ret_list


def _generate_token_sets(input_list):
    token_sets = _generate_parentheses(input_list)
    token_sets = _generate_functions(token_sets, input_list)
    token_sets = _generate_variables(token_sets, input_list)
    return _generate_numbers(token_sets, input_list)


def _generate_intermediates(current):
    ret_list = []
    for token_set in current:
        if token_set.token_set_type == number:
            ret_list.append(_INumber(token_set.start_index, token_set.end_index, token_set.token_list[0]))
        elif token_set.token_set_type == variable:
            ret_list.append(_IVariable(token_set.start_index, token_set.end_index, token_set.token_list[0]))
        elif token_set.token_set_type == parentheses:
            ret_list.append(
                _IParentheses(token_set.start_index, token_set.end_index, _generate_intermediate(token_set.token_list)))
        elif token_set.token_set_type == function:
            ret_list.append(_IFunction(token_set.start_index, token_set.end_index, token_set.representation,
                                       _generate_multiple_intermediates(token_set.token_list)))
    return ret_list


def _index_processed_operation(i, intermediate_list):
    for intermediate in intermediate_list:
        if intermediate.start_index <= i <= intermediate.end_index:
            return True
    return False


def _get_left_intermediate(i, intermediate_list):
    for intermediate in intermediate_list:
        if intermediate.start_index <= i - 1 <= intermediate.end_index:
            return intermediate
    return None


def _get_right_intermediate(i, intermediate_list):
    for intermediate in intermediate_list:
        if intermediate.start_index <= i + 1 <= intermediate.end_index:
            return intermediate
    return None


def _generate_identities(current, input_list):
    clone = []
    clone.extend(current)
    for i, token in enumerate(input_list):
        if not _index_processed_operation(i, clone):
            if token.token_type == tokens.operator:
                if token.representation == "+":
                    left = _get_left_intermediate(i, clone)
                    right = _get_right_intermediate(i, clone)
                    if left is None and right is not None:
                        clone.remove(right)
                        clone.append(_IIdentity(i, right.end_index, right))
                elif token.representation == "-":
                    left = _get_left_intermediate(i, clone)
                    right = _get_right_intermediate(i, clone)
                    if left is None and right is not None:
                        clone.remove(right)
                        clone.append(_INegation(i, right.end_index, right))

    ret_list = clone
    ret_list.sort(key=lambda x: x.start_index)
    return ret_list


def _generate_powers(current, input_list):
    clone = current
    for i, token in enumerate(input_list):
        if not _index_processed_operation(i, clone):
            if token.token_type == tokens.operator:
                if token.representation == "^":
                    left = _get_left_intermediate(i, clone)
                    right = _get_right_intermediate(i, clone)
                    if left is not None and right is not None:
                        clone.remove(left)
                        clone.remove(right)
                        clone.append(_IPower(left.start_index, right.end_index, left, right))
    ret_list = clone
    ret_list.sort(key=lambda x: x.start_index)
    return ret_list


def _generate_multiplication_and_division(current, input_list):
    clone = []
    clone.extend(current)
    for i, token in enumerate(input_list):
        if not _index_processed_operation(i, clone):
            if token.token_type == tokens.operator:
                if token.representation == "*":
                    left = _get_left_intermediate(i, clone)
                    right = _get_right_intermediate(i, clone)
                    if left is not None and right is not None:
                        clone.remove(left)
                        clone.remove(right)
                        clone.append(_IMultiplication(left.start_index, right.end_index, left, right))
                elif token.representation == "/":
                    left = _get_left_intermediate(i, clone)
                    right = _get_right_intermediate(i, clone)
                    if left is not None and right is not None:
                        clone.remove(left)
                        clone.remove(right)
                        clone.append(_IDivision(left.start_index, right.end_index, left, right))
    ret_list = clone
    ret_list.sort(key=lambda x: x.start_index)
    return ret_list


def _generate_addition_and_subtraction(current, input_list):
    clone = current
    for i, token in enumerate(input_list):
        if not _index_processed_operation(i, clone):
            if token.token_type == tokens.operator:
                if token.representation == "+":
                    left = _get_left_intermediate(i, clone)
                    right = _get_right_intermediate(i, clone)
                    if left is not None and right is not None:
                        clone.remove(left)
                        clone.remove(right)
                        clone.append(_IAddition(left.start_index, right.end_index, left, right))
                elif token.representation == "-":
                    left = _get_left_intermediate(i, clone)
                    right = _get_right_intermediate(i, clone)
                    if left is not None and right is not None:
                        clone.remove(left)
                        clone.remove(right)
                        clone.append(_ISubtraction(left.start_index, right.end_index, left, right))
    ret_list = clone
    ret_list.sort(key=lambda x: x.start_index)
    return ret_list


def _generate_operators(current, input_list):
    intermediates = _generate_identities(current, input_list)
    intermediates = _generate_powers(intermediates, input_list)
    intermediates = _generate_multiplication_and_division(intermediates, input_list)
    intermediates = _generate_addition_and_subtraction(intermediates, input_list)
    return intermediates


def _generate_multiple_intermediates(token_list):
    token_sets = _generate_token_sets(token_list)
    intermediates = _generate_intermediates(token_sets)
    intermediates = _generate_operators(intermediates, token_list)
    return intermediates


def _generate_intermediate(token_list) -> _Intermediate:
    intermediates = _generate_multiple_intermediates(token_list)
    if len(intermediates) == 1:
        return intermediates[0]
    else:
        raise ValueError("Unexpected error while generating intermediates")


def parse_operation(input_string):
    _validate_string(input_string)
    token_list = tokenizer.tokenize(input_string)
    _validate_syntax(token_list)
    intermediate_operation = _generate_intermediate(token_list)
    operation = intermediate_operation.compile()
    operation = operation.evaluate(variables.i, constant.i)
    operation = operation.evaluate(variables.j, constant.j)
    operation = operation.evaluate(variables.e, constant.e)
    return operation
