from collections import defaultdict
from functools import reduce
from itertools import product

from repTheory.BasicStructures import Perm, Algebraic
from repTheory.group_helpers import make_group


class SymmetrizerDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __contains__(self, item):
        if isinstance(item, Tableau):
            return str(item.type) in self.keys()
        return item in self.keys()


class Tableau:
    symmetrizer_map = SymmetrizerDict()

    @staticmethod
    def Y(s, t):
        if s.type != t.type:
            raise TypeError("Can not compute Y for different cycle types")
        # if t in Tableau.symmetrizer_map:
        #     alpha = (s.perm * ~t.perm)
        #     pi = ~t.perm * alpha * s.perm
        #     # print("optimized!")
        #     return pi.inv_conj(Tableau.symmetrizer_map[str(t.type)])

        return s.perm * t.symmetrizer()

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
    def combinations_of_order(n):
        return Tableau.combinations(*Tableau.tableau_of_order(n))

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

    @staticmethod
    def from_lists(rows):
        return Tableau([*map(len, rows)], perm=Perm.from_two_row([x for row in rows for x in row]))

    @staticmethod
    def tableau_of_order(n):
        return list(map(Tableau.from_lists, Tableau.raw_tableau_of_order(n)))

    @staticmethod
    def raw_tableau_of_order(n):
        if n <= 0:
            return []
        if n is 1:
            return [[[1]]]
        prev = Tableau.raw_tableau_of_order(n - 1)
        out = []
        for raw_tab in prev:
            for i in range(len(raw_tab)):
                if i and len(raw_tab[i - 1]) == len(raw_tab[i]):
                    continue
                new_tab = [inner.copy() for inner in raw_tab]
                new_tab[i].append(n)
                out.append(new_tab)

            out.append([*raw_tab, [n]])
        return out

    def __init__(self, type, perm=None):
        self.type = type
        self.size = sum(type)
        self.perm = Perm() if perm is None else perm

    def __str__(self):
        return " | ".join(" ".join(map(str, row)) for row in self.rows())

    def rows(self, type_rows=False):
        out = []
        last = 1
        for n in self.type:
            current = []
            for _ in range(n):
                current.append(last if type_rows else self.perm(last))
                last += 1
            out.append(current)
        return out

    def row_generators(self):
        return Tableau.all_two_cycles_of(self.rows())

    def columns(self, type_cols=False):
        cols = []
        if not len(self.type):
            return cols
        rows = self.rows(type_rows=type_cols)
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

    def type_symmetrizer(self):
        y = Algebraic()
        if str(self.type) in Tableau.symmetrizer_map:
            return Tableau.symmetrizer_map[str(self.type)]

        for gamma in make_group(Tableau.all_two_cycles_of(self.columns(type_cols=True))):
            for rho in make_group(Tableau.all_two_cycles_of(self.rows(type_rows=True))):
                y.terms[gamma * rho] += gamma.sign()

        Tableau.symmetrizer_map.setdefault(str(self.type), y)
        return y

    def symmetrizer(self):
        return self.perm.inv_conj(self.type_symmetrizer())

    def transpose(self):
        type = []
        old_type = self.type.copy()
        while old_type:
            type.append(len(old_type))
            old_type = [*filter(bool, map(lambda x: x - 1, old_type))]
        return Tableau(type, perm=Perm.from_two_row([x for col in self.columns() for x in col]))

    def is_standard(self):
        def ascending_list(list):
            if not len(list):
                return True
            return all(list[i] < list[i + 1] for i in range(len(list) - 1))

        return all(map(ascending_list, self.rows())) and all(map(ascending_list, self.columns()))

    def __repr__(self):
        return "Perm({0}{1})".format(self.perm, self.type)

    def fancy(self):
        max_len = len(str(self.size))

        def entry_to_str(entry):
            return str(entry) + (max_len - len(str(entry)) + 1) * " "
        return "\n".join(''.join(map(entry_to_str, row)) for row in self.rows())

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return isinstance(other, Tableau) and other.type == self.type and other.perm == self.perm
