
elem = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), (1, 0),
        (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (2, 0), (2, 1),
        (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (2, 11), (3, 0), (3, 1), (3, 2),
        (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11)]


def op(x, y):
    return (x[0] + y[0]) % 4, (x[1] + y[1]) % 12


def coset(a, b):
    out = set()
    if isinstance(a, list):
        for e in a:
            out.add(op(e, b))
    elif isinstance(b, list):
        for e in b:
            out.add(op(a, e))
    else:
        raise RuntimeError("One of the parameters must be str, the other must be list")

    return list(out)


def cyclic(a):
    last = a
    out = {last}
    while not last == (0, 0):
        last = op(last, (2, 2))
        out.add(last)
    out = list(out)
    out.sort(key=lambda x: elem.index(x))
    return out


