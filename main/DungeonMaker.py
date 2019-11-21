from enum import IntEnum


class Block(IntEnum):
    null = -2
    door = -1
    empty = 0
    wall = 1


def neighbors(empty_map, i, j):
    out = []

    for x in range(i - 1, min(i + 2, len(empty_map))):
        for y in range(j - 1, min(j + 2, len(empty_map[i]))):
            out.append(empty_map[x][y])

    out.remove(empty_map[i][j])

    return out


def make_boundaries(empty_map):
    for i in range(len(empty_map)):
        for j in range(len(empty_map[i])):
            if empty_map[i][j] != Block.empty:
                continue

            if i in [0, len(empty_map) - 1]:
                empty_map[i][j] = Block.wall
            elif j in [0, len(empty_map[i]) - 1]:
                empty_map[i][j] = Block.wall
            elif Block.null in neighbors(empty_map, i, j):
                empty_map[i][j] = Block.wall

    return empty_map


def make_division(bounded_map):
    # TODO: make a snakey division
    return bounded_map


def divide_map(bounded_map, n):
    for i in range(n):
        bounded_map = make_division(bounded_map)

    return bounded_map


def generate_room(empty_map):
    bounded_map = make_boundaries(empty_map)
    divided_map = divide_map(bounded_map, 6)
    return divided_map


def visualize_map(map):
    from PIL import Image
    from math import floor

    scalar = 5

    img = Image.new("RGB", (scalar * len(map), scalar * len(map[0])), color="white")
    img.format = "PNG"

    pixels = img.load()

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            block = map[floor(i / scalar)][floor(j / scalar)]

            if block == Block.null:
                pixels[i, j] = (0, 0, 0)
            elif block == Block.door:
                pixels[i, j] = (0, 100, 0)
            elif block == Block.wall:
                pixels[i, j] = (100, 0, 0)

    img.show()


if __name__ == '__main__':
    map = [[Block.null if i < 15 and 10 < j < 30 else Block.empty for i in range(40)] for j in range(40)]
    print(map)
    map = generate_room(map)
    visualize_map(map)
