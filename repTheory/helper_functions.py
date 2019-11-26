from numpy import array

from repTheory import Tableau


def symmetrizers_of_order(n):
    return map(lambda p: Tableau.Tableau.Y(*p), Tableau.Tableau.combinations_of_order(n))


def symmetrizer_matrix_of_order(n, ordering):
    return array(list(map(lambda s: s.to_coeffs(ordering), symmetrizers_of_order(n)))).transpose()


def print_matrix_with_order(matrix, ordering):
    max_len = max(len(str(p)) for p in ordering)
    def entry_to_str(entry):
        return " " * (3 - len(str(entry))) + str(entry)
    for i, p in enumerate(ordering):
        print(p, " " * (max_len - len(str(p))), *map(entry_to_str, matrix[i]), sep='')


def array_to_tex(array):
    return " \\\\\n".join(" & ".join(map(str, row)) for row in array)
