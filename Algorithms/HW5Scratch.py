import random


def rest_stops(possible, l):
    dist = 0
    i = 0
    stops = []

    possible.sort()

    if possible[i] - dist > 50:
        return None

    while i < len(possible) - 1 and possible[i + 1] - dist <= 50:
        i += 1

    stop = possible[i]
    stops.append(stop)
    dist = stop
    i += 1

    while i < len(possible) and 50 < l - dist:
        if possible[i] - dist > 100:
            return None

        while i < len(possible) - 1 and possible[i + 1] - dist <= 100:
            i += 1

        stop = possible[i]
        stops.append(stop)
        dist = stop
        i += 1

    if l - dist > 50:
        return None
    else:
        return stops


def test():
    length = random.randint(18, 35) * 10

    min = length // 50

    stops = [random.randint(1, (length - 1) // 10) * 10 for _ in range(random.randint(2*min, 3*min))]
    stops = list(set(stops))
    stops.sort()

    print(stops, " ", length)
    print(rest_stops(stops, length))


def staring_contest(a, b):
    a.sort()
    b.sort()

    out = list()
    for i in range(min(len(a), len(b))):
        t = a[i], b[i]
        out.append(t)

    return out


for i in range(20):
    test()
