from pyast import functions, variables, util
from pyast.parser.tokens import tokens

decimal = "."
valid_numbers = "0123456789."
operators = "+-*/^"
open_parenthesis = "("
close_parenthesis = ")"


def _pre_process(text: str):
    return text.replace(" ", "")


def _tokenize_numbers(input_string: str):
    ret_list = []
    accumulate = ""
    for i, v in enumerate(input_string):
        if v not in valid_numbers:
            if len(accumulate) != 0:
                start = i - len(accumulate)
                end = i - 1
                representation = accumulate
                number = tokens.Token(start, end, tokens.number, representation)
                ret_list.append(number)
                accumulate = ""
        else:
            accumulate += v
    if len(accumulate) != 0:
        start = len(input_string) - len(accumulate)
        end = len(input_string) - 1
        representation = accumulate
        number = tokens.Token(start, end, tokens.number, representation)
        ret_list.append(number)
    return ret_list


def _tokenize_operators(token_list, input_string: str):
    ret_list = []
    ret_list.extend(token_list)
    for i, v in enumerate(input_string):
        if not tokens.index_processed(i, ret_list):
            if v in operators:
                representation = v
                operator = tokens.single_index(i, tokens.operator)
                operator.representation = representation
                ret_list.append(operator)
    return ret_list


def _tokenize_parentheses(token_list, input_string: str):
    ret_list = []
    ret_list.extend(token_list)
    for i, v in enumerate(input_string):
        if not tokens.index_processed(i, ret_list):
            if v in open_parenthesis:
                representation = v
                parenthesis = tokens.single_index(i, tokens.open_parenthesis)
                parenthesis.representation = representation
                ret_list.append(parenthesis)
            elif v in close_parenthesis:
                representation = v
                parenthesis = tokens.single_index(i, tokens.close_parenthesis)
                parenthesis.representation = representation
                ret_list.append(parenthesis)
    return ret_list


def _tokenize_text(token_list, input_string: str):
    ret_list = []
    ret_list.extend(token_list)
    accumulated = ""
    for i, v in enumerate(input_string):
        if tokens.index_processed(i, ret_list):
            if len(accumulated) > 0:
                start = i - len(accumulated)
                end = i - 1
                representation = accumulated
                text = tokens.Token(start, end, tokens.text, representation)
                ret_list.append(text)
            accumulated = ""
        else:
            accumulated += v
    if len(accumulated) > 0:
        start = len(input_string) - len(accumulated)
        end = len(input_string) - 1
        representation = accumulated
        text = tokens.Token(start, end, tokens.text, representation)
        ret_list.append(text)
    ret_list.sort(key=lambda x: x.start_index)
    return ret_list


def _tokenize_functions(token_list):
    ret_list = []
    for i, curr in enumerate(token_list):
        if curr.token_type != tokens.text:
            ret_list.append(curr)
            continue
        if i < len(token_list) - 1 and token_list[i + 1].token_type == tokens.open_parenthesis:
            inner_func = ""
            found_inner = False
            representation = curr.representation
            for key in functions.reserved:
                if len(key) <= len(representation) and representation.endswith(key):
                    inner_func = key
                    found_inner = True
                    break
            if found_inner:
                end_index = representation.index(inner_func)
                if end_index != 0:
                    new_rep = representation[0:end_index]
                    rem = tokens.null_index(tokens.text, new_rep)
                    ret_list.append(rem)
                function = tokens.null_index(tokens.function, inner_func)
                ret_list.append(function)
            else:
                rem = curr.convert(tokens.text)
                ret_list.append(rem)
        else:
            rem = curr.convert(tokens.text)
            ret_list.append(rem)
    return ret_list


def _max_variables_in_string(input_string):
    ret_list = []
    max_var = ""
    max_count = -1
    for key in variables.reserved:
        if key in input_string and len(key) > max_count:
            max_var = key
            max_count = len(max_var)
    remaining_strings = util.find_remaining_strings(input_string, max_var)
    if max_count == -1 or len(remaining_strings) == 0:
        ret_list.append(tokens.null_index(tokens.variable, input_string))
        return ret_list
    if len(remaining_strings) == 1:
        if input_string.startswith(max_var):
            ret_list.append(tokens.null_index(tokens.variable, max_var))
            ret_list.extend(_max_variables_in_string(remaining_strings[0]))
            return ret_list
        left_hand_side = _max_variables_in_string(remaining_strings[0])
        ret_list.extend(left_hand_side)
        ret_list.append(tokens.null_index(tokens.variable, max_var))
        return ret_list
    if len(remaining_strings) == 2:
        left_hand_side = _max_variables_in_string(remaining_strings[0])
        right_hand_side = _max_variables_in_string(remaining_strings[1])
        ret_list.extend(left_hand_side)
        ret_list.append(tokens.null_index(tokens.variable, max_var))
        ret_list.extend(right_hand_side)
        return ret_list
    ret_list.append(tokens.null_index(tokens.variable, input_string))
    return ret_list


def _tokenize_variables(token_list):
    ret_list = []
    for curr in token_list:
        if curr.token_type != tokens.text:
            ret_list.append(curr)
        else:
            ret_list.extend(_max_variables_in_string(curr.representation))
    return ret_list


def _justify_mutliplication(input_list):
    ret_list = []
    for i, curr in enumerate(input_list):
        ret_list.append(curr)
        if curr.token_type == tokens.number or curr.token_type == tokens.variable or curr.token_type == tokens.close_parenthesis:
            if i < len(input_list) - 1 and input_list[i + 1].token_type != tokens.operator and input_list[
                i + 1].token_type != tokens.close_parenthesis:
                representation = "*"
                ret_list.append(tokens.null_index(tokens.operator, representation))
    return ret_list


def _collapse_signs(input_list):
    ret_list = []
    i = 0
    while i < len(input_list):
        curr = input_list[i]
        curr_representation = curr.representation
        next_representation = ""
        if i < len(input_list) - 1:
            next_representation = input_list[i + 1].representation
        if curr.token_type == tokens.operator and i < len(input_list) - 1 and input_list[
            i + 1].token_type == tokens.operator and (curr_representation == "+" or next_representation == "-") and (
                next_representation == "-" or curr_representation == "+"):
            representation = "+"
            if curr_representation != next_representation:
                representation = "-"
            ret_list.append(tokens.null_index(tokens.operator, representation))
            i += 2
        else:
            ret_list.append(curr)
            i += 1
    return ret_list


def _post_process(token_list):
    curr_list = _justify_mutliplication(token_list)
    collapsed = _collapse_signs(curr_list)
    while len(collapsed) != len(curr_list):
        curr_list = collapsed
        collapsed = _collapse_signs(curr_list)
    return curr_list


def tokenize(text: str):
    input_string: str = _pre_process(text)
    token_list = _tokenize_numbers(input_string)
    token_list = _tokenize_operators(token_list, input_string)
    token_list = _tokenize_parentheses(token_list, input_string)
    token_list = _tokenize_text(token_list, input_string)
    token_list = _tokenize_functions(token_list)
    token_list = _tokenize_variables(token_list)
    return _post_process(token_list)
