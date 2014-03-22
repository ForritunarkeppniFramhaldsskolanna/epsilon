
def check(expected, obtained):

    try:
        a = float(expected)
        b = float(obtained)
    except ValueError:
        return False

    return abs(a - b) <= 1e-3

