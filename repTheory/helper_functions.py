from numpy import array
from bisect import bisect
from repTheory import Tableaux
from repTheory.group_helpers import generateS


def symmetrizers_of_order(n):
    return map(lambda p: Tableaux.Tableau.Y(*p), Tableaux.Tableau.combinations_of_order(n))


def symmetrizer_matrix_of_order(n, ordering=None):
    return array(list(map(lambda s: s.to_coeffs(generateS(n) if not ordering else ordering), symmetrizers_of_order(n)))).transpose()


def print_matrix_with_ordering(matrix, ordering):  # , group_order=-1
    max_len = max(len(str(p)) for p in ordering)
    def entry_to_str(entry):
        return " " * (3 - len(str(entry))) + str(entry)

    # if group_order > -1:
    #     print_vertical(['  '*group_order, *map(lambda p: str(tuple(map(repr, p))),
    #     Tableaux.Tableau.combinations_of_order(group_order))])

    for i, p in enumerate(ordering):
        print(p, " " * (max_len - len(str(p))), *map(entry_to_str, matrix[i]), sep='')


def array_to_tex(array):
    return " \\\\\n".join(" & ".join(map(str, row)) for row in array)


def RSK(perm, preformatted=False):
    """Takes a permutation or the string form of a second row of a two row permutation and returns two Tableaux"""
    # Credit here:
    # https://mathoverflow.net/questions/30910/implementation-of-the-robinson-schensted-correspondence
    def fast_RSK(p):
        """Given the second row of a permutation p as a string, spit out a pair of Young tableaux as lists of lists"""
        P, Q = [], []
        def insert(m, n=0):
            '''Insert m into P, then place n in Q at the same place'''
            for r in range(len(P)):
                if m > P[r][-1]:
                    P[r].append(m)
                    Q[r].append(n)
                    return
                c = bisect(P[r], m)
                P[r][c], m = m, P[r][c]
            P.append([m])
            Q.append([n])

        for i in range(len(p)):
            insert(int(p[i]), i + 1)

        return P, Q

    formatted_input = perm if preformatted else ''.join(map(str, perm.to_two_row()))
    raw_output = fast_RSK(formatted_input)
    return tuple(map(Tableaux.Tableau.from_lists, raw_output))


def array_to_mathematica(array):
    return "{ " + ", \n".join("{ " + ", ".join(map(str, row)) + " }" for row in array) + " }"


def print_vertical(columns, **print_kwargs):
    for i in range(max(map(len, columns))):
        print(*iter(s[i] if i < len(s) else ' ' for s in columns), **print_kwargs)
