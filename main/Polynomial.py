class Polynomial:
    def __init__(self, coeff):
        self.coeff = coeff

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Polynomial) and o.coeff == self.coeff

    def __repr__(self):
        return '(' + ' + '.join(str(v) + 'x^' + str(i) for i, v in enumerate(self.coeff) if v is not 0) + ')'

    def __iter__(self):
        return iter(self.coeff)

    def __add__(self, other):
        if isinstance(other, Polynomial):
            new = [0] * max(len(self.coeff), len(other.coeff))

            def getAt(list, i):
                if len(list) <= i:
                    return 0
                return list[i]

            for i in range(max(len(self.coeff), len(other.coeff))):
                new[i] += getAt(self.coeff, i) + getAt(other.coeff, i)
            return Polynomial(new)

    def __sub__(self, other):
        if isinstance(other, Polynomial):
            new = [0] * max(len(self.coeff), len(other.coeff))

            def getAt(list, i):
                if len(list) <= i:
                    return 0
                return list[i]

            for i in range(max(len(self.coeff), len(other.coeff))):
                new[i] += getAt(self.coeff, i) - getAt(other.coeff, i)
            return Polynomial(new)

    def __mul__(self, other):
        if isinstance(other, Polynomial):
            def getAt(list, i):
                if len(list) <= i:
                    return 0
                return list[i]

            new = list()

            for i, v in enumerate(other.coeff):
                if v is 0:
                    continue
                add = ([0] * i) + ([v * n for n in self.coeff])
                new = [getAt(new, i) + getAt(add, i) for i in range(max(len(add), len(new)))]

            return Polynomial(new)
        elif isinstance(other, int):
            return Polynomial([other * n for n in self.coeff.copy()])

    def __pow__(self, power, modulo=None):
        assert isinstance(power, int)
        if power is 0:
            return Polynomial([1])
        factor = Polynomial(self.coeff)
        result = factor
        for i in range(power - 1):
            result *= factor
        return result

    def __len__(self):
        s = 0
        for i in self.coeff:
            if i != 0:
                s += 1
        return s


if __name__ == '__main__':
    p = Polynomial([1, 0, 0, 3, 4.3])
    q = Polynomial([0, 2, 0, 3, -1.3])

    print(p)
    print(q)
    print(p + q)
    print(p - q)
