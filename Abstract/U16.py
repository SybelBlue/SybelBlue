# This is an automatically generated python file 
# generated on 2019-03-20 22:19:15.903768 

# This is a U_16 group 
n = 16

# The element list of U_16 
elem = [1, 3, 5, 7, 9, 11, 13, 15]


# The standard operation for U_16
def op(x, y):
    return (x * y) % n


# The standard Cayley Table making function for U_16 in dictionary form 
def make_table(elem, op):
    out = {}
    for a in elem:
        for b in elem:
            out[(a, b)] = op(a, b)
    return out


# The Cayley table for U_16
table = {(1, 1): 1, (1, 3): 3, (1, 5): 5, (1, 7): 7, (1, 9): 9, (1, 11): 11, (1, 13): 13, (1, 15): 15, (3, 1): 3, 
         (3, 3): 9, (3, 5): 15, (3, 7): 5, (3, 9): 11, (3, 11): 1, (3, 13): 7, (3, 15): 13, (5, 1): 5, 
         (5, 3): 15, (5, 5): 9, (5, 7): 3, (5, 9): 13, (5, 11): 7, (5, 13): 1, (5, 15): 11, (7, 1): 7, 
         (7, 3): 5, (7, 5): 3, (7, 7): 1, (7, 9): 15, (7, 11): 13, (7, 13): 11, (7, 15): 9, (9, 1): 9, 
         (9, 3): 11, (9, 5): 13, (9, 7): 15, (9, 9): 1, (9, 11): 3, (9, 13): 5, (9, 15): 7, (11, 1): 11, 
         (11, 3): 1, (11, 5): 7, (11, 7): 13, (11, 9): 3, (11, 11): 9, (11, 13): 15, (11, 15): 5, (13, 1): 13, 
         (13, 3): 7, (13, 5): 1, (13, 7): 11, (13, 9): 5, (13, 11): 15, (13, 13): 9, (13, 15): 3, (15, 1): 15, 
         (15, 3): 13, (15, 5): 11, (15, 7): 9, (15, 9): 7, (15, 11): 5, (15, 13): 3, (15, 15): 1}

def latex_cayley():
    str = "\\[\\begin{array}{ l | cccccccc }\n & "
    str += " & ".join([x.__str__() for x in elem]) + "\\\\\n" 
    str += "\\hline \n" 
    for e in elem:
        str += e.__str__() + " & " + " & ".join([table[e, x].__str__() for x in elem]) + " \\\\\n"
    str += "\\end{array}\\]"
    return str


def coset(a, b):
    out = set()
    if isinstance(a, list) and isinstance(b, int):
        for e in a:
            out.add(op(e, b))
    elif isinstance(a, int) and isinstance(b, list):
        for e in b:
            out.add(op(a, e))
    else:
        raise RuntimeError("One of the parameters must be str, the other must be list")

    return list(out)


def coset_op(a, b):
    out = set()
    for i in a:
        for j in b:
            out.add(op(i, j))
    return list(out)


H = [1, 15]
K = [1, 9]

for i in elem:
    for j in elem:
        if i <= j < 9:
            print(i, " ", j)
            print(coset_op(coset(i, H), coset(j, H)))
