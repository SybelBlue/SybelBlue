from main.Polynomial import Polynomial


def rectify(func):
    def final(*args):
        poly = Z2Poly(func(*args))
        return poly
    return final


class Z2Poly(Polynomial):
    def __init__(self, coeff):
        super().__init__(coeff)
        self.coeff = [n % 2 for n in self.coeff]

    @rectify
    def __add__(self, other):
        return super(Z2Poly, self).__add__(other)

    @rectify
    def __sub__(self, other):
        return super(Z2Poly, self).__sub__(other)

    @rectify
    def __mul__(self, other):
        return super(Z2Poly, self).__mul__(other)

    @rectify
    def __pow__(self, power, modulo=None):
        return super(Z2Poly, self).__pow__(power, modulo=modulo)

    def __str__(self):
        return super(Z2Poly, self).__str__().replace('1x', 'x')

    def __repr__(self):
        return super(Z2Poly, self).__repr__().replace('1x', 'x')


polys = [Z2Poly(x) for x in [[i, j] for i in range(2) for j in range(2)]]
print(polys)
