from math import factorial
from numpy import array

from repTheory import Tableau
from repTheory.BasicStructures import Perm


def generateS(n):
    return make_group([Perm([i + 1, i + 2]) for i in range(n - 1)], group_limit=factorial(n))


# def generateA(n):
#     return make_group([Perm([i + 1, i + 2, i + 3]) for i in range(n - 2)], group_limit=factorial(n)/2)


def make_group(generators, group_limit=10000):
    group = [*generators]
    last_len = 0
    while last_len != len(group) and last_len < group_limit:
        last_len = len(group)
        for item in generators:
            group.extend([*map(item, group)])
            group = list(set(group))

    return group


def symmetrizers_of_order(n):
    return map(lambda p: Tableau.Tableau.Y(*p), Tableau.Tableau.combinations_of_order(n))


def symmetrizer_matrix_of_order(n, ordering):
    return array([*map(lambda s: s.to_coeffs(ordering), symmetrizers_of_order(n))]).transpose()


def print_matrix_with_order(matrix, ordering):
    max_len = max(len(str(p)) for p in ordering)
    def entry_to_str(entry):
        return " " * (3 - len(str(entry))) + str(entry)
    for i, p in enumerate(ordering):
        print(p, " " * (max_len - len(str(p))), *map(entry_to_str, matrix[i]), sep='')


def array_to_tex(array):
    return " \\\\\n".join(" & ".join(map(str, row)) for row in array)
