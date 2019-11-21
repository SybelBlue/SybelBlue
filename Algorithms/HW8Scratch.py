from csv import DictReader


def face_saver(games, k):
    table = dict()
    n = len(games)
    for i in range(n):
        table[i, 0] = 0
    for i in range(k + 1):
        table[-1, i] = 0
        table[-2, i] = 0

    for i in range(1, k + 1):
        for j in range(n):
            cancelled = table[j - 2, i - 1]
            played = table[j - 1, i]
            curr_game = games[j]
            table[j, i] = max(curr_game + cancelled, played)

    result = table[n - 1, k]

    i = n - 1
    j = k
    value = result
    cancelled = list()
    while i >= 0:
        if table[i - 1, j] != value:
            cancelled.append(games[i])
            j -= 1
            i -= 2
            value -= games[i]
        else:
            i -= 1

    return result, cancelled


def knapsack(capacity, weights, values):
    table = dict()
    n = len(weights)
    for w in range(capacity + 1):
        table[0, w] = 0
    for i in range(n):
        table[i, 0] = 0
    for i in range(1, n):
        for w in range(1, capacity + 1):
            if weights[i] > w:
                table[i, w] = table[i - 1, w]
            else:
                table[i, w] = max(table[i - 1, w], values[i] + table[i - 1, w - weights[i]])

    result = table[n - 1, capacity]

    i = n - 1
    j = capacity
    value = result
    nabbed = list()
    while i > 0:
        if table[i - 1, j] != value:
            nabbed.append(i + 1)
            value -= values[i]
            while table[i - 1, j] != value:
                j -= 1
        i -= 1

    return result, nabbed


def is_hybrid(hybrid, a, b):
    if len(hybrid) != len(a) + len(b):
        return False

    table = dict()
    for i in range(len(a)):
        n = i + len(b)
        table[i, len(b)] = (hybrid[n:] == a[i:])
    for i in range(len(b)):
        n = i + len(a)
        table[len(a), i] = (hybrid[n:] == b[i:])

    for i in reversed(range(len(a))):
        for j in reversed(range(len(b))):
            n = i + j
            table[i, j] = (a[i] == hybrid[n] and table[i + 1, j]) or (b[j] == hybrid[n] and table[i, j + 1])

    return table[0, 0]


if __name__ == '__main__':
    with open('res/shortListOfGames.csv', newline='') as csv_file:
        reader = DictReader(csv_file)
        file_dict = {int(row['wallopingScore']): row['school'] for row in reader}
        points = list(file_dict.keys())
        solution = face_saver(points, 3)
        result = [file_dict[n] for n in solution[1]]
        print('Maximized value in shortListOfGames: ', solution[0])
        print(', '.join(result))

    with open('res/knapsackItems.csv', newline='') as csv_file:
        reader = DictReader(csv_file)
        file_dict = {(int(row['weight']), int(row['value'])): row['item'] for row in reader}
        weights = [k[0] for k in file_dict.keys()]
        values = [k[1] for k in file_dict.keys()]
        solution = knapsack(11, weights, values)
        print('Maximized value in knapsackItems: ', solution[0])
        print(', '.join([str(i) for i in solution[1]]))

    test_params = 'goodhbyeello', 'hello', 'goodbye'
    print(is_hybrid(*test_params))
