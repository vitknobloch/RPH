DIGIT_DICT = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}

def sum_digits(string):
    sum = 0
    for c in string:
        if(c in DIGIT_DICT):
            sum += DIGIT_DICT[c]
    return sum

def sum_digits_alt(string):
    return sum([int(s) for s in string if s in '0123456789'])
