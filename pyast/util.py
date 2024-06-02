def contains_left(one_list, other_list):
    for one in one_list:
        if one not in other_list:
            return False
    return True


def contains_all(one_list, other_list):
    if len(one_list) != len(other_list):
        return False
    return set(one_list) == set(other_list)


def find_remaining_strings(test, key):
    if len(key) == 0:
        return []
    if key not in test:
        return []
    if len(key) == len(test):
        return []
    index = test.index(key)
    if index == 0:
        return [test[len(key):]]
    if test.endswith(key):
        return [test[0:(len(test) - len(key))]]
    else:
        return [
            test[0:index],
            test[index + len(key):]
        ]
