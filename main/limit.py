def lim(f, t):
    step = 1 if len(t) < 2 else t[1]
    i = f(t[0])
    accum = i
    for n in range(i + step, 100000000, step):
        i = f(n)
        accum += i

    return accum


print(lim(lambda x: x ** -2, (1, 1)))
