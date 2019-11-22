from collections import defaultdict


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
