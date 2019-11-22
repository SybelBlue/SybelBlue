from collections import defaultdict


class Tableau:
    def __init__(self, type, perm=None):
        self.type = type
        self.perm = Perm() if perm is None else perm

    def __str__(self):
        return "Perm({0}{1})".format(self.perm, self.type)


class Perm:
    @staticmethod
    def fromTwoRow(second_row):
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

        return Perm(cycles)

    def __init__(self, cycles=None):
        if cycles is None or not len(cycles):
            cycles = [[]]
        elif isinstance(cycles[0], int) or (isinstance(cycles, list) and not len(cycles)):
            cycles = [cycles]
        self.is_identity = cycles == [[]]
        self.cycles = cycles
        self.max_value = 1 if self.is_identity else max(x for cycle in cycles for x in cycle)

    def __str__(self):
        return "(1)" if self.is_identity else "".join("(" + " ".join(map(str, cycle)) + ")" for cycle in self.cycles)

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
        if not isinstance(other, Perm):
            raise NotImplementedError("Can't multiply non-Perm objects")
        if self.is_identity:
            return other

        return Perm.fromTwoRow([self(other(i + 1)) for i in range(max(self.max_value, other.max_value))])


class Algebraic:
    def __init__(self, term_map=None):
        if term_map is None:
            term_map = defaultdict(lambda: 0)
        self.termMap = term_map

    def __add__(self, other):
        if isinstance(other, Perm):
            self.termMap[other] += 1
        elif isinstance(other, Algebraic):
            for k, v in other.termMap.items():
                self.termMap[k] += v

    def __rmult__(self, other):
        if isinstance(other, Algebraic):
            raise NotImplementedError("Haven't done Algebraic times Algebraic yet")
        if isinstance(other, Perm):
            return Algebraic({other(k): v for k, v in self.termMap.items()})

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

        return " + ".join(filter(len, (str_of_term(v, k) for k, v in self.termMap.items())))


assert [*map(Perm([[1, 2, 3], [4, 7]]), [2, 3, 4, 9])] == [3, 1, 7, 9] # can be used as function, int application works
assert str(Perm()) == "(1)" # tests that the identity works
assert str(Perm.fromTwoRow([4, 1, 3, 2, 6, 5])) == "(1 4 2)(5 6)" # conversion from classic 2 x n mat. (second row only)
assert (Perm([1, 2]) * Perm([3, 4])).cycles == Perm([[1, 2], [3, 4]]).cycles # multiplication and single-cycle syntax

random_elem = Algebraic({Perm([[1, 2, 3]]): 2, Perm([[1, 3, 2]]): 1, Perm(): -1, Perm([[1, 2]]): 0})
print(random_elem)

print(Perm([1, 2]) * random_elem)

print(Perm([[2, 3]])(4))
