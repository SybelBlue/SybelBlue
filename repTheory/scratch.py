from collections import defaultdict
from math import factorial


class Tableau:
    def __init__(self, type, perm=None):
        self.type = type
        self.size = sum(type)
        self.perm = Perm() if perm is None else perm

    def __str__(self):
        return "Perm({0}{1})".format(self.perm, self.type)

    def rows(self):
        out = []
        last = 1
        for n in self.type:
            current = []
            for _ in range(n):
                current.append(self.perm(last))
                last += 1
            out.append(current)
        return out

    def row_generators(self):
        return list({*map(Perm, self.rows())})

    def columns(self):
        cols = []
        if not len(self.type):
            return cols
        rows = self.rows()
        for i in range(self.type[0]):
            col = []
            for j in range(len(self.type)):
                if len(rows[j]) <= i:
                    break
                col.append(self.perm(rows[j][i]))
            cols.append(col)

        return cols

    def col_genenerators(self):
        return list({*map(Perm, self.columns())})

    def __repr__(self):
        space = " " * len(str(self.size))
        return "\n".join(space.join(map(str, row)) for row in self.rows())


class Perm:
    """ Assuemd to be disjoint when init """

    @staticmethod
    def to_two_row(perm):
        return [perm(i + 1) for i in range(perm.max_value)]

    @staticmethod
    def from_two_row(second_row):
        remaining = [x + 1 for x in range(len(second_row))]
        cycles = []
        while remaining:
            i = remaining.pop(0)
            current = second_row[i - 1]
            if i is current:  # if its i -> i, skip this one
                continue

            cycle = [i]
            while i is not current:  # keep going till you get back to i
                remaining.remove(current)
                cycle.append(current)
                current = second_row[current - 1]

            cycles.append(cycle)

        return Perm.from_lists(cycles)

    @staticmethod
    def from_lists(lists):
        return Perm(*lists)

    def __init__(self, *cycles):
        cycles = list(cycles)
        if cycles is None or not len(cycles) or len(cycles) == 1 == len(cycles[0]):
            cycles = [[]]
        elif isinstance(cycles[0], int) or (isinstance(cycles, list) and not len(cycles)):
            cycles = [cycles]

        self.is_identity = cycles == [[]]
        self.cycles = cycles
        self.max_value = 1 if self.is_identity else max(x for cycle in cycles for x in cycle)

    def __str__(self):
        return "(1)" if self.is_identity else "".join("(" + " ".join(map(str, cycle)) + ")" for cycle in self.cycles)

    def __repr__(self):
        return str(self)

    def apply(self, n):
        if not isinstance(n, int):
            raise NotImplementedError("Can not apply to non int types: " + str(n))
        for cycle in self.cycles:
            found = False
            for m in cycle:
                if found:
                    return m
                if m is n:
                    found = True
            if found:
                return cycle[0]
        return n

    def compose_with(self, other):
        """ returns (self o other) """
        if self.is_identity:
            return other

        return Perm.from_two_row([self(other(i + 1)) for i in range(max(self.max_value, other.max_value))])

    def inverse(self):
        def cycle_inverse(cycle):
            return [cycle[0], *(cycle[1:])[::-1]]

        return Perm.from_lists(map(cycle_inverse, self.cycles))

    def scrub(self):
        cycles = []
        for cycle in self.cycles:
            if len(cycle) <= 1:
                continue

            index = cycle.index(min(cycle))
            cycles.append(cycle[index:] + cycle[:index])

        self.cycles = sorted(cycles, key=lambda cycle: cycle[0])
        return self

    def __neg__(self):
        print(self)

    def __call__(self, *args, **kwargs):
        """ so that permutations can be applied like functions to ints or other perms """
        if len(args) != 1 or len(kwargs):
            raise NotImplementedError("Can only pass one element")
        arg = args[0]
        if isinstance(arg, Perm):
            return self * arg

        return self.apply(arg)

    def __mul__(self, other):
        if isinstance(other, Algebraic):
            return other.__rmult__(self)
        if isinstance(other, int) or isinstance(other, float):
            return Algebraic({self: other})
        if not isinstance(other, Perm):
            raise NotImplementedError("Can't multiply non-Perm and non-Algebraic objects")

        return self.compose_with(other)

    def __rmul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Algebraic({self: other})
        raise NotImplementedError("Can't rmul " + other + " and Algebraic")

    def __truediv__(self, other):
        return ~self * other

    def __eq__(self, other):
        if self is other:
            return True

        def test_cycles(i):
            return all(self.cycles[i][j] == other.cycles[i][j] for j in range(len(self.cycles[i])))

        return len(self.cycles) is len(other.cycles) and all(test_cycles(i) for i in range(len(self.cycles)))

    def __hash__(self):
        return hash(str(self))

    def __invert__(self):
        return self.inverse()


class Algebraic:
    def __init__(self, term_map=None):
        if term_map is None:
            term_map = defaultdict(lambda: 0)
        self.terms = term_map

    def __iadd__(self, other):
        if isinstance(other, Perm):
            self.terms[other] += 1
        elif isinstance(other, Algebraic):
            for k, v in other.terms.items():
                self.terms[k] += v
        return self

    def __isub__(self, other):
        if isinstance(other, Perm):
            self.terms[other] -= 1
        elif isinstance(other, Algebraic):
            for k, v in other.terms.items():
                self.terms[k] -= v
        return self

    def __add__(self, other):
        terms = self.terms.copy()
        if isinstance(other, Perm):
            terms[other] += 1
        elif isinstance(other, Algebraic):
            for k, v in other.terms.items():
                terms[k] += v
        return Algebraic(terms)

    def __sub__(self, other):
        terms = self.terms.copy()
        if isinstance(other, Perm):
            terms[other] -= 1
        elif isinstance(other, Algebraic):
            for k, v in other.terms.items():
                terms[k] -= v
        return Algebraic(terms)

    def scale(self, other):
        return Algebraic({k: other * v for k, v in self.terms.items()})

    def __mul__(self, other):
        return other.__rmult__(self)

    def __rmult__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.scale(other)
        if isinstance(other, Algebraic):
            test = Algebraic()
            for k, v in self.terms.items():
                test += k * self.scale(v)
            return test
        if isinstance(other, Perm):
            return Algebraic({other(k): v for k, v in self.terms.items()})
        raise NotImplementedError()

    def __str__(self):
        def str_of_term(coeff, perm):
            if not coeff:
                return ""
            if perm.is_identity:
                return str(coeff)
            if coeff is 1:
                return str(perm)
            if coeff is -1:
                return "-" + str(perm)
            return str(coeff) + str(perm)

        out = " + ".join(filter(len, (str_of_term(v, k) for k, v in self.terms.items())))
        return out if len(out) else "0"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self is other or (isinstance(other, Algebraic) and other.terms == self.terms)

    def __hash__(self):
        return hash(self.terms)


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