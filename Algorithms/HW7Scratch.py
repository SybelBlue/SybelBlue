from random import randint
from csv import DictReader
from math import sqrt


class Notebook(list):
    def __init__(self, size=8, avoid=None):
        super().__init__()
        if avoid is None:
            avoid = list()
        values = set()
        while len(values) < size:
            n = randint(0, size * size)
            if avoid is None or n not in avoid:
                values.add(n)
        values = sorted(list(values))
        self.extend(values)

    def query(self, k):
        return self.__getitem__(k - 1)

    def __repr__(self):
        return super().__repr__()


def winner_value(j1, j2, bound1=None, bound2=None):
    if bound1 is None:
        bound1 = (0, len(judge1))
        bound2 = (0, len(judge2))

    if bound1[1] - bound1[0] == 1:
        return min(j1[bound1[0]], j2[bound2[0]])

    mid_line1 = (bound1[1] - bound1[0]) // 2 + bound1[0]
    mid_line2 = (bound2[1] - bound2[0]) // 2 + bound2[0]

    mid_value1 = j1.query(mid_line1)
    mid_value2 = j2.query(mid_line2)

    if mid_value1 > mid_value2:
        bound1 = bound1[0], mid_line1
        bound2 = mid_line2, bound2[1]
        return winner_value(j1, j2, bound1, bound2)
    else:
        bound2 = bound2[0], mid_line2
        bound1 = mid_line1, bound1[1]
        return winner_value(j1, j2, bound1, bound2)


def closest_pair_in(points):
    p_x = sorted(points, key=lambda x: x[0])
    p_y = sorted(points, key=lambda x: x[1])

    return closest_pair(p_x, p_y)


def closest_pair(p_x, p_y):
    if len(p_x) <= 3:
        return brute_force(p_x)

    mid_cut = len(p_x) // 2
    mid_x = p_x[mid_cut]

    left_x = p_x[:mid_cut]
    right_x = p_x[mid_cut:]

    left_y = [p for p in p_y if p[0] <= mid_x[0]]
    right_y = [p for p in p_y if p[0] > mid_x[0]]

    del_l, p_l, q_l = closest_pair(left_x, left_y)
    del_r, p_r, q_r = closest_pair(right_x, right_y)

    delta = min(del_l, del_r)

    if delta == del_l:
        out = delta, p_l, q_l
    else:
        out = delta, p_r, q_r

    close_to_line = [p for p in p_y if mid_x[0] - delta <= p[0] <= mid_x[0] + delta]

    for i, p in enumerate(close_to_line):
        for q in close_to_line[i + 1: i + 8]:
            d_close = dist(p, q)
            if d_close < out[0]:
                out = d_close, p, q

    return out


def brute_force(p):
    closest = None, None, None
    for a in p:
        for b in p:
            if a == b:
                continue

            d = dist(a, b)
            if closest[0] is None or d < closest[0]:
                closest = d, a, b

    return closest


def dist(a, b):
    return sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]))


def test_file(file_name):
    with open('res/' + file_name + '.csv', newline='') as csv_file:
        avatar_reader = DictReader(csv_file)
        file_dict = {(float(row['Latitude']), float(row['Longitude'])): row['Feature'] for row in avatar_reader}
        points = file_dict.keys()
        solution = closest_pair_in(points)
        result = [file_dict[v] for v in solution if isinstance(v, tuple)]
        print('Minimum distance in', file_name, ': ', solution[0])
        print(', '.join(result))


if __name__ == '__main__':
    judge1 = Notebook()
    judge2 = Notebook(avoid=judge1)
    print("judge 1:", judge1)
    print("judge 2:", judge2)
    print("median is:", winner_value(judge1, judge2))

    print("Closest locations:")
    test_file('worldOfAvatar')
    test_file('chicagoLocations')
    test_file('minnesotaLocations')
