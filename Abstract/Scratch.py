from itertools import permutations

out = []
for item in permutations(range(1,5), 3):
    item = list(item)
    out.append(item[::2])
print(out)
