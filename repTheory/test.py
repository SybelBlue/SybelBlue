from functools import reduce

from repTheory.BasicStructures import Perm, Algebraic
from repTheory.Tableau import Tableau, symmetrizers_of_order, convert_to_TeX
from repTheory.groups import generateS

from numpy import array

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

print("---")
s_3_pairs = [*Tableau.combinations_of_order(3)]
s_3_pairs[3], s_3_pairs[4] = s_3_pairs[4], s_3_pairs[3]
print(*map(lambda p: (str(p[0]), str(p[1])), s_3_pairs))
symmetrizers = list()
for i, pair in enumerate(s_3_pairs):
    y = Tableau.Y(*pair)
    symmetrizers.append(y)
    print(i, pair, y)

mat = array([*map(lambda s: s.to_coeffs(ordering), symmetrizers)]).transpose()
print(mat)
print(convert_to_TeX(mat))

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
symmetrizers = symmetrizers_of_order(4)

mat = array([*map(lambda s: s.to_coeffs(ordering), symmetrizers)]).transpose()
print(mat)
