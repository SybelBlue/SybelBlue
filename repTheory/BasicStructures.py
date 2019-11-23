from collections import defaultdict


class Perm:
    """ Assumed to be disjoint on init """

    @staticmethod
    def to_two_row(perm):
        return [perm(i + 1) for i in range(perm.max_value())]

    @staticmethod
    def from_two_row(second_row, to_check=None):
        remaining = [x + 1 for x in range(len(second_row))] if to_check is None else to_check
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
        self.__max_value__ = 1 if self.is_identity else None
        self.__scrubbed__ = False

    def __len__(self):
        return sum(map(len, self.cycles))

    def max_value(self):
        if self.__max_value__:
            return self.__max_value__
        self.__max_value__ = max(x for cycle in self.cycles for x in cycle)
        return self.__max_value__

    def sign(self):
        # self.scrub()
        return 1 if self.is_identity else ((len(self) - len(self.cycles)) % 2) * -2 + 1

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

        return Perm.from_two_row([self(other(i + 1)) for i in range(max(self.max_value(), other.max_value()))])

    def inverse(self):
        if self.is_identity:
            return Perm()
        def cycle_inverse(cycle):
            return [cycle[0], *(cycle[1:])[::-1]]

        return Perm.from_lists(map(cycle_inverse, self.cycles))

    def scrub(self):
        if self.__scrubbed__:
            return self

        self.__scrubbed__ = True
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
        raise NotImplementedError("Can't rmul " + str(other) + " and Algebraic")

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

    def __pow__(self, power, modulo=None):
        if power < 0:
            return (~self) ** (-power)
        current = Perm()
        for _ in range(power):
            current *= self
        return current

    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Algebraic({self: 1, Perm(): other})
        return Algebraic({self: 1, other: 1})

    def __sub__(self, other):
        return Algebraic({self: 1, other: -1})


class Algebraic:
    def __init__(self, term_map=None):
        self.terms = defaultdict(lambda: 0)
        if term_map is None:
            return
        for k, v in term_map.items():
            self.terms[k] = v

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
        terms = defaultdict(lambda: 0)
        for k, v in self.terms.items():
            terms[k] = v

        if isinstance(other, Perm):
            terms[other] += 1
        elif isinstance(other, Algebraic):
            for k, v in other.terms.items():
                terms[k] += v
        return Algebraic(terms)

    def __sub__(self, other):
        terms = defaultdict(lambda: 0)
        for k, v in self.terms.items():
            terms[k] = v

        if isinstance(other, Perm):
            terms[other] -= 1
        elif isinstance(other, Algebraic):
            for k, v in other.terms.items():
                terms[k] -= v
        return Algebraic(terms)

    def scale(self, other):
        return Algebraic({k: other * v for k, v in self.terms.items()})

    def normalized(self):
        return self.scale(1 / sum(map(abs, self.terms.values())))

    def __mul__(self, other):
        if isinstance(other, Perm):
            return Algebraic({k(other): v for k, v in self.terms.items()})
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
        raise TypeError("Perm.__rmult__ is not defined for " + str(other))

    def __getitem__(self, item):
        return self.terms[item]

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
        if self is other:
            return True
        if not isinstance(other, Algebraic):
            return False

        return all(not v or other.terms[k] == v for k, v in self.terms.items())

    def __hash__(self):
        return hash(str(self))

    def to_coeffs(self, ordering):
        return [self[perm] for perm in ordering]
