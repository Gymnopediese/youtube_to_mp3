def remove_from_to(string: str, a, b):
    if a not in string or b not in string:
        return string
    string = string[:string.index(a)] + string[string.index(b) + 1:]
    return string