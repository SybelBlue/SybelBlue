import random

class Node:
    value = 0
    parent = None
    childA = None
    childB = None

    def __init__(self, value):
        self.value = value

    def __str__(self):
        if self.childA is None and self.childB is None:
            return str(self.value)
        return str(self.value) + '{' + str(self.childA) + ',' + str(self.childB) + '}'

    def formatted_tree(self, n=1):
        if self.childA is None and self.childB is None:
            return '\t' + str(self.value)
        t = n + 1
        return str(self.value) + '{\n' + n * '\t' + self.childA.formatted_tree(
            n=t) + ',\n' + n * '\t' + self.childB.formatted_tree(n=t) + '}'

    def __bool__(self):
        return self.childA is not None and self.childB is not None

    def __gt__(self, other):
        return other.__lt__(self.value)

    def __lt__(self, other):
        return other.__gt__(self.value)


def bind(parent: Node, child: Node):
    if parent.childA is None:
        parent.childA = child
    elif parent.childB is None:
        parent.childB = child

    child.parent = parent


def randomNode():
    return Node(random.randint(1, 100))


def build_deep(parent, depth):
    if depth == 1:
        return
    new = randomNode()
    bind(parent, new)
    build_deep(new, depth - 1)
    new = randomNode()
    bind(parent, new)
    build_deep(new, depth - 1)


def local_min(node):
    parent = node.parent is None or node < node.parent
    child_a = node.childA is None or node < node.childA
    child_b = node.childB is None or node < node.childB

    if parent and child_a and child_b:
        return node

    if node.childA < node.childB:
        return local_min(node.childA)

    return local_min(node.childB)


# tree = randomNode()
# build_deep(tree, 4)
# print(tree.formatted_tree())
# print(local_min(tree))


person_values = [bool(random.getrandbits(1)) for _ in range(random.randint(10, 15))]
fill_factor = lambda arr: sum(1 for x in arr if x) / len(arr)
while fill_factor(person_values) <= 0.5:
    person_values[random.randint(0, len(person_values) - 1)] = True


def evaluate(a, b):
    return person_values[b] if person_values[a] else True


def find_good(people):
    if len(people) == 1:
        return people[0]
    elif len(people) == 0:
        return None

    new = []
    p_iter = iter(people)
    for a, b in zip(p_iter, p_iter):
        if evaluate(a, b) == evaluate(b, a):
            new.append(a)

    res = find_good(new)

    if res is not None:
        return res

    if not len(people) % 2:
        return None

    return people[-1]


def find_all_good(people):
    truthful = find_good(people)
    good = [n for n in people if evaluate(truthful, n)]
    return good


# print(len(person_values))
# print([n for n, v in enumerate(person_values) if v])
# print(find_all_good(list(range(len(person_values)))))

for l in range(40, 100):
    people = list(range(l))
    person_values = [bool(random.getrandbits(1)) for _ in people]
    while fill_factor(person_values) <= 0.5:
        person_values[random.randint(0, len(person_values) - 1)] = True

    assert [n for n, v in enumerate(person_values) if v] == find_all_good(people)

print('All good.')
