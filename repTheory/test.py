from math import factorial

from repTheory.BasicStructures import Perm, Algebraic
from repTheory.Tableau import Tableau


def generateS(n):
    generators = [Perm([i + 1, i + 2]) for i in range(n - 1)]

    group = [Perm(), *generators]
    while len(group) < factorial(n):
        for perm in generators:
            group.extend([*map(perm, group)])  # DONT UNBOX! WILL CAUSE INFINITE LOOPING
            group = list(set(group))

    return group


assert Perm([1, 2]) == Perm([1, 2])  # basic equality test
assert Perm([5, 4], [], [2, 3, 1]).scrub() == Perm([1, 2, 3], [4, 5])  # test scrubbing into standard form
assert [*map(Perm([1, 2, 3], [4, 7]), [2, 3, 4, 9])] == [3, 1, 7, 9]  # can be used as function, int application works
assert str(Perm()) == "(1)"  # tests that the identity and str(identity) works
assert str(
    Perm.from_two_row([4, 1, 3, 2, 6, 5])) == "(1 4 2)(5 6)"  # conversion from classic 2 x n mat. (second row only)
assert (Perm([1, 2]) * Perm([3, 4])).cycles == Perm([1, 2], [3, 4]).cycles  # multiplication and single-cycle syntax

test_cycle = Perm([1, 2, 3], [4, 7])
assert ~test_cycle * test_cycle == Perm()  # inverse test
assert test_cycle / test_cycle == Perm()  # division test

random_elem = Algebraic({Perm([1, 2, 3]): 2, Perm([1, 3, 2]): 1, Perm(): -1, Perm([1, 2]): 0})
assert random_elem == random_elem  # basic equality test
assert random_elem.terms[Perm([1, 2, 3])] is 2  # Perm hash works

print(random_elem - 2 * Perm([1, 2, 3]))
print(Algebraic({Perm([1, 2, 3]): 1, Perm(): 1}))
random_elem -= Perm([1, 2, 3])

print(random_elem.scale(2))

print(random_elem - random_elem)
print(Perm([1, 2]) * random_elem)
print(random_elem * random_elem)

print(Perm([2, 3])(4))

print(generateS(3))

ex_tableau = Tableau([3, 2, 2, 1, 1])
print(repr(ex_tableau))
print(ex_tableau.row_generators())

print(ex_tableau.col_genenerators())


print(repr(Tableau([3, 2, 2], perm=Perm([3, 6, 4]))))