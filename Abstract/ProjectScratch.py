from Abstract.GroupST import *
from Abstract.LaTeXFunctions import formatted_cols


def hw2_25():
    g0 = ["e", "s"]
    g1 = ["e", "s", "tstt", "ttst"]
    g2 = ["e", "st", "tts"]
    groups = [g0, g1, g2]

    results = []
    for group in groups:
        for item in elem:
            results.append(coset(group, item))
        for item in elem:
            results.append(coset(item, group))

    reduced = []
    for res in results:
        reduced_coset = [reduce(e) for e in res]
        reduced_coset.sort(key=elem.index)
        reduced.append(reduced_coset)

    finals = [reduced[12 * i:12 * (i + 1)] for i in range(6)]

    print(formatted_cols(finals, elem))
