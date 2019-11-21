import random

directions = ['up', 'down', 'left', 'right']


class Cell:
    def __init__(self, i, j):
        self.pos = i, j
        self.visited = False
        self.walls = {x: True for x in directions}

    def move_to(self, other):
        if self.pos[0] < other.pos[0]:
            self.walls['right'] = False
            other.walls['left'] = False
        elif self.pos[0] > other.pos[0]:
            other.walls['right'] = False
            self.walls['left'] = False
        elif self.pos[1] < other.pos[1]:
            self.walls['down'] = False
            other.walls['up'] = False
        elif self.pos[1] > other.pos[1]:
            other.walls['down'] = False
            self.walls['up'] = False


cols, rows = 10, 10
grid = [[Cell(i, j) for j in range(cols)] for i in range(rows)]


def neighbor(cell):
    out = []

    def safe_add(a, b):
        if a < 0 or b < 0:
            return
        if a >= cols or b >= rows:
            return
        item = grid[a][b]
        if not item.visited:
            out.append(item)
    i, j = cell.pos

    safe_add(i - 1, j)
    safe_add(i, j - 1)
    safe_add(i + 1, j)
    safe_add(i, j + 1)

    if not out:
        return None

    return random.choice(out)


current = grid[0][0]
stack = [current]


def print_grid():
    def get_str_at(i, j):
        def safe_check(a, b, s):
            if a < 0 or b < 0:
                return False
            if a >= cols or b >= rows:
                return False
            return grid[a][b].walls[s]
        center = grid[i][j]
        # up = center.walls['up'] or safe_check(i - 1, j, 'down')
        # right = center.walls['right'] or safe_check(i - 1, j, 'left')
        left = center.walls['left'] or safe_check(i - 1, j, 'right')
        down = center.walls['down'] or safe_check(i, j + 1, 'up')

        s = '|' if left else ' '
        s += '_' if down else ' '
        # s += '|' if right else '_'
        return s

    for i in range(rows):
        for j in range(cols):
            print(get_str_at(i, j), end='')
        print()


while stack:
    current.visited = True
    next = neighbor(current)
    if next is not None:
        current.move_to(next)
        stack.append(current)
        current = next
        print_grid()
    else:
        current = stack.pop()

print_grid()
