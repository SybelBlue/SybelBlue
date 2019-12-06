from functools import reduce

import numpy
import sympy

from repTheory.BasicStructures import Perm, Algebraic
from repTheory.Tableaux import Tableau

from numpy import array

from repTheory.group_helpers import generateS
from repTheory.helper_functions import array_to_tex, symmetrizer_matrix_of_order, print_matrix_with_ordering, RSK, \
    array_to_mathematica, print_vertical

assert Perm([1, 2]) == Perm([1, 2])  # basic equality test
assert Perm([5, 4], [], [2, 3, 1]).scrub() == Perm([1, 2, 3], [4, 5])  # test scrubbing into standard form
assert Perm([1, 2, 3], [4, 5]) == Perm([1, 2, 3], [4, 5]).scrub()  # test scrubbing does nothing to standard form
assert [*map(Perm([1, 2, 3], [4, 7]), [2, 3, 4, 9])] == [3, 1, 7, 9]  # can be used as function, int application works
assert str(Perm()) == "(1)"  # tests that the identity and str(identity) works
assert str(Perm.from_two_row([4, 1, 3, 2, 6, 5])) == "(1 4 2)(5 6)"  # conversion from 2xN mat form. (second row only)
assert (Perm([1, 2]) * Perm([3, 4])).cycles == Perm([1, 2], [3, 4]).cycles  # multiplication and single-cycle syntax

test_cycle = Perm([1, 2, 3], [4, 7])
assert ~test_cycle * test_cycle == Perm()  # inverse test
assert test_cycle / test_cycle == Perm()  # division test
assert test_cycle.sign() is -1  # sign test
assert len(set(test_cycle ** i for i in range(6))) is 6  # pow test
assert test_cycle.inv_conj(Perm([1, 4, 2, 3])) == test_cycle * Perm([1, 4, 2, 3]) * ~test_cycle

test_elem = Algebraic({Perm([1, 2, 3]): 3, Perm([1, 3, 2]): 1, Perm(): -1, Perm([1, 2]): 0})
assert test_elem == test_elem  # basic equality test
assert test_elem[Perm([1, 2, 3])] is 3  # Perm hash works, Algebraic getitem works

# Alg-Perm subtraction, Perm mutliplication and Algebraic equality
assert test_elem - 2 * Perm([1, 2, 3]) == Algebraic({Perm([1, 2, 3]): 1, Perm([1, 3, 2]): 1, Perm(): -1})
test_elem += Perm([1, 2, 3])
test_elem -= 2 * Perm([1, 2, 3])
# Alg subtract-equals, plus-equals, equality, Perm __rmult__
assert test_elem == Algebraic({Perm([1, 2, 3]): 2, Perm([1, 3, 2]): 1, Perm(): -1})

# Alg scaling, __mul__
assert test_elem * 2 == 4 * Perm([1, 2, 3]) + 2 * Perm([1, 3, 2]) - 2 * Perm()
# Alg 0
assert test_elem - test_elem == Algebraic()

# Alg __rumlt__ and key rotation
assert test_elem * Perm([1, 2]) == 2 * Perm([1, 3]) + Perm([2, 3]) - Perm([1, 2])
# Alg __mul__ and key rotation
assert Perm([1, 2]) * test_elem == 2 * Perm([2, 3]) + Perm([1, 3]) - Perm([1, 2])
assert Perm([1, 2]) * test_elem * ~Perm([1, 2]) == Perm([1, 2]).inv_conj(test_elem)

# Alg x Alg
assert test_elem * (2 * Perm([1, 2])) == 4 * Perm([1, 3]) + 2 * Perm([2, 3]) - 2 * Perm([1, 2])
assert test_elem * test_elem == 2 * Perm([1, 3, 2]) - 3 * Perm([1, 2, 3]) + 5 * Perm()

# generator tests
assert len(set(generateS(3))) is 6
assert len(set(generateS(4))) is 24
assert len(set(generateS(5))) is 120

assert Tableau([2, 1]) == Tableau.from_lists([[1, 2], [3]])
assert Tableau([2, 1], perm=Perm([2, 3])) == Tableau.from_lists([[1, 3], [2]])
assert all(map(lambda t: t.is_standard(), Tableau.tableau_of_order(5)))

assert RSK('1364752', preformatted=True) == RSK(Perm.from_two_row([1, 3, 6, 4, 7, 5, 2]))

# print(*sorted(generateS(4),  key=lambda perm: perm.key()))
# print(*map(lambda p: p.key(), sorted(generateS(4),  key=lambda perm: perm.key())))
# print(len({*map(lambda p: p.key(), sorted(generateS(4),  key=lambda perm: perm.key()))}))

test_tableau = Tableau([4, 2, 2, 1], perm=Perm())
print("tableau")
print(test_tableau.fancy())
print("repr:", repr(test_tableau))
print("row generators:", *test_tableau.row_generators())
print("column generators:", *test_tableau.col_generators())
print(reduce(lambda p, q: p + q, test_tableau.col_generators()))
print("transpose")
print(test_tableau.transpose().fancy())

print("-------")
test_tableau = Tableau([2, 1])
print(test_tableau.fancy())
print("symmet:", test_tableau.symmetrizer())
test_pair = Tableau([2, 1], perm=Perm([2, 3])), test_tableau
print(*test_pair)
test_Y = Tableau.Y(*test_pair)
print(test_Y)
# ordering = sorted(generateS(3), key=lambda perm: perm.key())
ordering = [Perm(), Perm([1, 2]), Perm([1, 3]), Perm([2, 3]), Perm([1, 3, 2]), Perm([1, 2, 3])]
print(ordering)
print(test_tableau.symmetrizer().to_coeffs(ordering))
print(test_Y.to_coeffs(ordering))


def get_stats_on_mat(mat):
    print('-------- STATS FOR NERDS ----------')
    print(numpy.sum(mat, axis=0))
    print("det:", numpy.linalg.det(mat))
    print("tr:", numpy.trace(mat))
    print('----------------------------------')


print("---")
s_3_pairs = Tableau.combinations_of_order(3)
# s_3_pairs[3], s_3_pairs[4] = s_3_pairs[4], s_3_pairs[3]
print(*map(lambda p: (str(p[0]), str(p[1])), s_3_pairs))
symmetrizers = list()
for i, pair in enumerate(s_3_pairs):
    y = Tableau.Y(*pair)
    symmetrizers.append(y)
    print(i, pair, y)

mat = array([*map(lambda s: s.to_coeffs(ordering), symmetrizers)]).transpose()
get_stats_on_mat(mat)
print_matrix_with_ordering(mat, ordering)
print(array_to_tex(mat))

print()
print()
print("---")
ordering = sorted(generateS(4), key=lambda perm: perm.key())
# s_4_pairs = Tableau.combinations_of_order(4)
# symmetrizers = list()
# for i, pair in enumerate(s_4_pairs):
#     y = Tableau.Y(*pair)
#     symmetrizers.append(y)
#     print(i, pair, y)
# ordering = generateS(4)
mat = symmetrizer_matrix_of_order(4, ordering)
get_stats_on_mat(mat)
print_matrix_with_ordering(mat, ordering)
# print(array_to_tex(mat))
print(array_to_mathematica(mat))

test_elem = Tableau([3, 2]).symmetrizer()
print(len(test_elem))

# s_5 = sorted(generateS(5), key=lambda perm: perm.key())
# print(next(x for x in s_5 if x not in test_elem))
# mat = symmetrizer_matrix_of_order(5, s_5)
# print_matrix_with_order(mat, s_5)
# get_stats_on_mat(mat)

# test_tableau = Tableau([4, 3, 3, 2], perm=Perm([4, 7, 5]))
# print(test_tableau.fancy())
# print()
# print(test_tableau.transpose().fancy())
# print()
# print(test_tableau.perm, '*', test_tableau.transpose().perm, '=', test_tableau.perm * test_tableau.transpose().perm)

# cycle_type = [3, 1]
# ordering = generateS(4)
# print(list(map(lambda cycle: Tableau.Y(Tableau(cycle_type), Tableau(cycle_type, perm=Perm([3, 4])))[cycle], ordering)))
# print(list(map(lambda cycle: Tableau.Y(Tableau(cycle_type).transpose(), Tableau(cycle_type, perm=Perm([3, 4])).transpose())[cycle], ordering)))

# print(*map(lambda tab: tab.fancy(), RSK('1364752', preformatted=True)), sep='\n')
test_cycle = Perm.from_two_row([1, 3, 6, 4, 7, 5, 2])
print(test_cycle, *RSK(test_cycle), sep='\n')

# all tableaux generated by RSK are standard.
# ordering = sorted(generateS(3), key=lambda p: p.key())
# print(*zip(iter(ordering), map(RSK, ordering), Tableau.combinations_of_order(3)), sep='\n')
# print(*zip(iter(ordering), map(RSK, ordering)), sep='\n')
# print(all(map(lambda p: all(map(lambda t: t.is_standard(), p)), map(RSK, ordering))))
