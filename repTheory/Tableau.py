from collections import defaultdict
from functools import reduce
from itertools import product

from repTheory.BasicStructures import Perm, Algebraic
from repTheory.groups import make_group


class Tableau:
    @staticmethod
    def Y(r, t):
        if r.type != t.type:
            raise TypeError("Can not compute Y for different cycle types")
        sig = (r.perm * ~t.perm)
        return ~sig * t.symmetrizer() * sig

    @staticmethod
    def all_two_cycles_of(lists):
        out = list()
        for row in lists:
            for i in range(len(row) - 1):
                out.append(Perm([row[i], row[i + 1]]))
        if not len(out):
            out.append(Perm())
        return out

    @staticmethod
    def combinations(*tabs):
        """ returns all pairings of provided tabs that can be entered as params in Tableau.Y """
        def add_and_ret(d, k, v):
            d[k].append(v)
            return d

        out = []
        groupings = reduce(lambda d, tab: add_and_ret(d, str(tab.type), tab), tabs, defaultdict(list)).values()
        for grouping in groupings:
            for pair in product(grouping, grouping):
                out.append(pair)
        return out


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
        return Tableau.all_two_cycles_of(self.rows())

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
                col.append(rows[j][i])
            cols.append(col)

        return cols

    def col_generators(self):
        return Tableau.all_two_cycles_of(self.columns())

    def symmetrizer(self):
        y = Algebraic()
        for gamma in make_group(self.col_generators()):
            for rho in make_group(self.row_generators()):
                y.terms[gamma * rho] += gamma.sign()
        return y

    def transpose(self):
        """ structural transpose only!!! does not preserve labeling """
        type = []
        old_type = self.type.copy()
        while old_type:
            type.append(len(old_type))
            old_type = [*filter(bool, map(lambda x: x - 1, old_type))]
        return Tableau(type)

    def __repr__(self):
        return " | ".join(" ".join(map(str, row)) for row in self.rows())

    def fancy(self):
        space = " " * len(str(self.size))
        return "\n".join(space.join(map(str, row)) for row in self.rows())
