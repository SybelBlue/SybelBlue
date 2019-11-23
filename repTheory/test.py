from functools import reduce

from repTheory.BasicStructures import Perm, Algebraic
from repTheory.Tableau import Tableau
from repTheory.groups import generateS

assert Perm([1, 2]) == Perm([1, 2])  # basic equality test
assert Perm([5, 4], [], [2, 3, 1]).scrub() == Perm([1, 2, 3], [4, 5])  # test scrubbing into standard form
assert [*map(Perm([1, 2, 3], [4, 7]), [2, 3, 4, 9])] == [3, 1, 7, 9]  # can be used as function, int application works
assert str(Perm()) == "(1)"  # tests that the identity and str(identity) works
assert str(Perm.from_two_row([4, 1, 3, 2, 6, 5])) == "(1 4 2)(5 6)"  # conversion from 2xN mat form. (second row only)
assert (Perm([1, 2]) * Perm([3, 4])).cycles == Perm([1, 2], [3, 4]).cycles  # multiplication and single-cycle syntax

test_cycle = Perm([1, 2, 3], [4, 7])
assert ~test_cycle * test_cycle == Perm()  # inverse test
assert test_cycle / test_cycle == Perm()  # division test
assert test_cycle.sign() is -1  # sign test
assert len(set(test_cycle ** i for i in range(6))) is 6  # pow test

test_elem = Algebraic({Perm([1, 2, 3]): 3, Perm([1, 3, 2]): 1, Perm(): -1, Perm([1, 2]): 0})
assert test_elem == test_elem  # basic equality test
assert test_elem[Perm([1, 2, 3])] is 3  # Perm hash works, Algebraic getitem works

print(test_elem - 2 * Perm([1, 2, 3]))
print(Algebraic({Perm([1, 2, 3]): 1, Perm(): 1}))
test_elem -= Perm([1, 2, 3])

print(test_elem.scale(2))

print(test_elem - test_elem)
print(test_elem * Perm([1, 2]))
print(Perm([1, 2]) * test_elem)
print(~Perm([1, 2]) * test_elem * Perm([1, 2]))
print(test_elem * test_elem)

assert len(set(generateS(3))) is 6
assert len(set(generateS(4))) is 24
assert len(set(generateS(5))) is 120

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
print(test_tableau.symmetrizer())
test_Y = Tableau.Y(Tableau([2, 1], perm=Perm([2, 3])), test_tableau)
print(test_Y)
ordering = sorted(generateS(3), key=lambda perm: perm.key())
print(ordering)
print(test_Y.to_coeffs(ordering))

print(Tableau.combinations(Tableau([3]), Tableau([2, 1]), Tableau([2, 1], perm=Perm([2, 3])), Tableau([1, 1, 1])))
