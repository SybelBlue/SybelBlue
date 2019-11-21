#     |   |   | 1 |   |   |
#     | 1 |   | 1 |   |   |
#     | 1 | 4 | 1 | 3 | 1 |
# -------------------------
#   1 |   |   | # |   |   |
# -------------------------
#   2 | # | # |   |   |   |
# -------------------------
#   3 |   | # | # | # |   |
# -------------------------
# 2 1 | # | # |   | # |   |
# -------------------------
#   4 |   | # | # | # | # |
# -------------------------


class Nonogram:
    def __init__(self, clues, size=5):
        self.clues = clues
        self.size = size
        self.solution = [['0' for _ in range(size)] for _ in range(size)]
        self.toCheck = None

    def offer(self, elem):
        self.toCheck.insert(0, elem)

    def poll(self):
        return self.toCheck.pop()

    def solve(self):
        self.toCheck = list(range(-self.size, self.size))
        checked = [False] * (self.size * 2)
        while self.toCheck:
            current = self.poll()

            if current < 0:  # row
                index = -current - 1
                clue = self.clues[1][index]
                match = self.parse(clue, self.solution[index])
                if match is not None:
                    self.solution[index] = match
                    for i in range(self.size):
                        if not checked[i + self.size] and i not in self.toCheck:
                            self.offer(i)
                    checked[current + self.size] = not any(x == '0' for x in match)
            else:  # col
                clue = self.clues[0][current]
                match = self.parse(clue, [x[current] for x in self.solution])
                if match is not None:
                    for i, x in enumerate(self.solution):
                        x[current] = match[i]
                    for i in range(-self.size, 0):
                        if not checked[i + self.size] and i not in self.toCheck:
                            self.offer(i)
                    checked[current + self.size] = not any(x == '0' for x in match)

        return self.present()

    @staticmethod
    def count(coll):
        return sum(1 for n in coll if n == '1')

    def parse(self, clue, string):
        if 2 * len(clue) - 1 is self.size:
            return list('X'.join(['1'*c for c in clue]))

        cluesum = sum(clue)

        if cluesum == self.count(string):
            return ['1' if n == '1' else 'X' for n in string]

        editted = False
        pieces = ''.join(string).split(sep='X')

        start = 0
        while len(pieces[start]) < clue[0]:
            start += 1

        end = len(pieces) - 1
        while len(pieces[end]) < clue[-1]:
            end -= 1

        if end - start + 1 == len(clue):
            res = pieces[:start] if start > 0 else []
            for i, v in enumerate(clue):
                piece = pieces[i + start]
                if v == len(piece):
                    res.append('1' * v)
                    editted = True
                elif v > len(piece) / 2:
                    lower, upper = len(piece) - v, v
                    res.append(piece[:lower] + '1' * (upper - lower) + piece[upper:])
                    editted = True
                else:
                    res.append(piece)
            if editted:
                if end < len(pieces) - 1:
                    string = list('X'.join(res + pieces[:(end + 1)]))
                else:
                    string = list('X'.join(res))

        if cluesum == self.count(string):
            return ['1' if n == '1' else 'X' for n in string]

        return string if editted else None

    def present(self):
        return tuple(tuple(1 if entry == '1' else 0 for entry in row) for row in self.solution)

    def __str__(self):
        return str(self.solution)


clues = (((1, 1), (4,), (1, 1, 1), (3,), (1,)),
         ((1,), (2,), (3,), (2, 1), (4,)))

ans = ((0, 0, 1, 0, 0),
       (1, 1, 0, 0, 0),
       (0, 1, 1, 1, 0),
       (1, 1, 0, 1, 0),
       (0, 1, 1, 1, 1))

clues = (((1,), (3,), (1,), (3, 1), (3, 1)),
          ((3,), (2,), (2, 2), (1,), (1, 2)))

ans = ((0, 0, 1, 1, 1),
       (0, 0, 0, 1, 1),
       (1, 1, 0, 1, 1),
       (0, 1, 0, 0, 0),
       (0, 1, 0, 1, 1))

non = Nonogram(clues, size=15)
sol = non.solve()


print(non)
print(sol)

assert sol == ans
#         i = 0
#         j = 0
#         res = ''
#         need_gap = False
#         while i < len(string) and j < len(clue):
#             if need_gap or string[i] == 'X':
#                 need_gap = False
#                 i += 1
#                 res += 'X'
#                 continue
#
#             c = 0
#             while (string[i] == '1' or string[i] == 0) and c < clue[j]:
#                 c += 1
#                 i += 1
#
#             if c == clue[j]:
#                 res += '1' * clue[j]
#                 j += 1
#                 need_gap = True
#                 continue
#
#             res += 'X'
#             i += 1
#
#         if j == len(clue) and i == len(string):
#             return list(res)
