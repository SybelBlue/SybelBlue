from repTheory.BasicStructures import Perm


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
