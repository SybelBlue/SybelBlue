def rest_stops(d, x):
    for n in d:
        if n > x:
            return None

    dist, i = 0, 0
    stops = []
    n = len(d)
    while i < n:
        while i < n and dist + d[i] <= x:
            dist += d[i]
            i += 1

        if i < n:
            stops.append(i - 1)
            dist = 0

    return stops


def alpha(a, b):
    if a is None or b is None:
        return -1
    if a != b:
        return -1
    return 2


def align(big, small):
    if len(big) < len(small):
        return align(small, big)

    table: dict = {(-1, -1): (0, None)}
    for i in range(len(big)):
        table[i, -1] = (0, None)
    for i in range(len(small)):
        table[-1, i] = (0, None)

    for i in range(len(big)):
        for j in range(len(small)):
            options = [alpha(big[i], small[j]) + table[i - 1, j - 1][0],
                              alpha(big[i], None) + table[i - 1, j][0],
                              alpha(None, small[j]) + table[i, j - 1][0]]
            table[i, j] = max(options)
            table[i, j] = (table[i, j], options.index(table[i, j]))

    out = table[len(big) - 1, len(small) - 1]
    tracker_i = len(big) - 1
    tracker_j = len(small) - 1
    for i in range(len(big)):
        if table[i, len(small) - 1][0] > out[0]:
            out = table[i, len(small) - 1]
            tracker_i = i

    print(tracker_i, tracker_j, out)

    s = '_' * (len(big) - tracker_i - 1)
    while out[1] is not None:
        if out[1] == 0:
            s += small[tracker_j]
            tracker_j -= 1
            tracker_i -= 1
        elif out[1] == 1:
            s += '-'
            tracker_i -= 1
        else:
            s += small[tracker_j]
            tracker_j -= 1
        out = table[tracker_i, tracker_j]

    s += '_' * (len(big) - len(s))

    return ''.join(reversed(s))


teststr = "caaccacaWXXZaaaaaaWXaaYZa"
print(align(teststr, 'WXYZ'))
print(teststr)
