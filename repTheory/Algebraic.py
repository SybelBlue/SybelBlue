from collections import defaultdict
from repTheory.Perm import Perm


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
