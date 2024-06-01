def contains_left(one_list, other_list):
    for one in one_list:
        if one not in other_list:
            return False
    return True


def contains_all(one_list, other_list):
    if len(one_list) != len(other_list):
        return False
    return set(one_list) == set(other_list)
