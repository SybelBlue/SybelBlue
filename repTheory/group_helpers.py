from math import factorial

from repTheory.BasicStructures import Perm


def generateS(n):
    return make_group([Perm([i + 1, i + 2]) for i in range(n - 1)], group_limit=factorial(n))


def make_group(generators, group_limit=10000):
    group = [*generators]
    last_len = 0
    while last_len != len(group) and last_len < group_limit:
        last_len = len(group)
        for item in generators:
            group.extend([*map(item, group)])
            group = list(set(group))

    return group
