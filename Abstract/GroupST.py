from itertools import combinations

elem = ["e", "s", "t", "st", "ts", "tt", "sts", "stt", "tts", "tst", "ttst", "tstt"]

table = {'ee': 'e', 'es': 's', 'et': 't', 'se': 's', 'te': 't', 'st': 'st', 'sst': 't', 'sts': 'sts', 'stt': 'stt',
         'ssts': 'ts', 'sstt': 'tt', 'stts': 'tst', 'stst': 'tts', 'sttst': 'tstt', 'ststt': 'ttst', 'tst': 'tst',
         'tts': 'tts', 'ttt': 'e', 'tsts': 'stt', 'tstt': 'tstt', 'ttts': 's', 'ttst': 'ttst', 'tttst': 'st',
         'ttstt': 'sts', 'sttt': 's', 'ststs': 'tt', 'sttts': 'e', 'stttst': 't', 'sttstt': 'ts', 'tssts': 'tts',
         'tsstt': 'e', 'tstts': 'ttst', 'tstst': 's', 'tsttst': 'sts', 'tststt': 'st', 'ttsts': 'tstt', 'tttts': 'ts',
         'ttttst': 'tst', 'tttstt': 'stt', 'stsstt': 's', 'ststts': 'tstt', 'ststst': 'e', 'ststtst': 'ts',
         'stststt': 't', 'stttts': 'sts', 'sttttst': 'tts', 'stttstt': 'tt', 'ttstst': 'ts', 'ttsttst': 'stt',
         'ttststt': 'tst', 'tstttst': 'tt', 'tsttstt': 'tts', 'ttsttstt': 's', 'ss': 'e', 'tss': 't', 'tsst': 'tt',
         'tttt': 't', 'stss': 'st', 'stsst': 'stt', 'stssts': 'tst', 'stttt': 'st', 'sttsts': 'ttst', 'ttss': 'tt',
         'ttsst': 'e', 'ttssts': 'tst', 'ttsstt': 't', 'ttstts': 'st', 'tsttt': 'ts', 'tststs': 'e', 'tsttts': 't',
         'ttsttt': 'tts', 'ttststs': 't', 'ttsttts': 'tt', 'ttstttst': 'e', 'tstttt': 'tst', 'tsttsts': 'st',
         'tstttts': 'stt', 'tsttttst': 's', 'tstttstt': 'e'}

reduction_map = {'ttsttstt': 's', 'ttstttst': 'e', 'tsttttst': 's', 'tstttstt': 'e', 'stststt': 't', 'ttststs': 't',
                 'ststst': 'e', 'stttst': 't', 'stsstt': 's', 'ststtst': 'ts', 'stttstt': 'tt', 'tstttst': 'tt',
                 'ttsstt': 't', 'tststs': 'e', 'tsttts': 't', 'ttsttts': 'tt', 'tsttsts': 'st', 'tstst': 's',
                 'ttstst': 'ts', 'ttsst': 'e', 'tsstt': 'e', 'sttts': 'e', 'sttstt': 'ts', 'tststt': 'st',
                 'sttttst': 'tts', 'ttsttst': 'stt', 'ttststt': 'tst', 'tsttstt': 'tts', 'ttstts': 'st',
                 'tstttts': 'stt', 'ststs': 'tt', 'tsttst': 'sts', 'ttts': 's', 'tttst': 'st', 'sttt': 's',
                 'tttts': 'ts', 'ttttst': 'tst', 'tttstt': 'stt', 'stttts': 'sts', 'tttt': 't', 'stssts': 'tst',
                 'stttt': 'st', 'ttssts': 'tst', 'tsttt': 'ts', 'ttsttt': 'tts', 'tstttt': 'tst', 'ttstt': 'sts',
                 'ttt': 'e', 'sst': 't', 'ssts': 'ts', 'sstt': 'tt', 'tssts': 'tts', 'ststts': 'tstt', 'tss': 't',
                 'tsst': 'tt', 'stss': 'st', 'stsst': 'stt', 'sttsts': 'ttst', 'ttss': 'tt', 'stts': 'tst',
                 'ststt': 'ttst', 'sttst': 'tstt', 'tstts': 'ttst', 'ttsts': 'tstt', 'tsts': 'stt', 'stst': 'tts',
                 'ss': 'e', 'es': 's', 'et': 't', 'se': 's', 'te': 't', 'ee': 'e'}

rainbow_tree = ['e', 's', 't', 0, 'st', 'ts', 'tt', -1, -1, 'sts', 'stt', 2, 'tst', 'tts', 0, -1, -1, -1, -1, 4, 13,
                12, 1, -1, -1, 10, 'tstt', 6, 'ttst', -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                -1, -1, -1, -1, -1, -1, -1, -1, 28, 5, -1, -1, 26, 9, -1, -1, -1, -1]


def sort(collection):
    collection.sort(key=lambda e: elem.index(e))
    return collection


def unique_repr(collection):
    return str(sort(list({x for x in collection})))


def reduce(raw):
    if len(raw) > 400:
        return reduce_long(raw)

    last_pos = 0
    last_entry = 'e'

    for char in raw:
        if char is 'e':
            continue
        elif char is 's':
            next_pos = 2 * last_pos + 1
        else:
            next_pos = 2 * last_pos + 2

        next_entry = rainbow_tree[next_pos]
        if type(next_entry) is int:
            last_pos = next_entry
            last_entry = rainbow_tree[next_entry]
        else:
            last_pos = next_pos
            last_entry = next_entry

    return last_entry


# use only when len(raw) > 500. Otherwise substantially slower than reduce
def reduce_long(raw):
    entry = raw

    for _ in range(len(raw)):
        for target, repl in reduction_map.items():
            entry = entry.replace(target, repl)

        if entry in elem:
            break

    return entry


def coset(a, b):
    if isinstance(a, list) and isinstance(b, str):
        out = set(reduce(e + b) for e in a)
    elif isinstance(a, str) and isinstance(b, list):
        out = set(reduce(a + e) for e in b)
    else:
        raise RuntimeError("One of the parameters must be str, the other must be list")

    return sort(list(out))


def subgroup(*a):
    a = [reduce(x) for x in a]
    cyclic = a.copy()
    to_process = a.copy()

    while to_process and len(cyclic) < len(elem):
        current = to_process.copy()
        to_process.clear()
        for item in current:
            for old in cyclic:
                n = reduce(item + old)
                if not (n in cyclic or n in current):
                    cyclic.append(n)
                    if n not in to_process:
                        to_process.append(n)
                n = reduce(old + item)
                if not (n in cyclic or n in current):
                    cyclic.append(n)
                    if n not in to_process:
                        to_process.append(n)

    return sort(cyclic)


def is_generator(*a):
    return len(subgroup(*a)) == len(elem)


def subgroups():
    results = {"['e']": ['e']}
    for i in range(1, len(elem)):
        for comb in combinations(elem[1:], i):
            if len(comb) == 1:
                comb = comb[0]
            s = subgroup(*comb)
            sort(s)
            key = unique_repr(s)
            results[key] = s
    return list(results.values())


def subgroup_generators():
    results = {"['e']": ['e']}
    for i in range(1, len(elem)):
        for comb in combinations(elem[1:], i):
            if len(comb) == 1:
                comb = comb[0]
            s = subgroup(*comb)
            key = unique_repr(s)
            if key not in results:
                results[key] = [comb]
            else:
                results[key].append(comb)

    return results


def op(a, b):
    return reduce(a + b)


def inv(a):
    for b in elem:
        if op(a, b) == 'e':
            return b
    return None


def is_normal(H):
    return all([sort(coset(a, coset(H, inv(a)))) == H for a in elem])


def is_abelian(H):
    for i in H:
        for j in H:
            if not op(i, j) == op(j, i):
                return False
    return True


def commutor():
    out = set()
    for i in elem:
        for j in elem:
            out.add(reduce(inv(i) + inv(j) + i + j))
    return sort(list(out))


def quotient_group(Q):
    return None if len(elem) % len(Q) else {unique_repr(coset(k, Q)): sort(list(coset(k, Q))) for k in elem}.values()


def print_subgroup_generators():
    for k, v in subgroup_generators().items():
        print(k, "(", len(v), "): ", v)


def conjugacy_classes():
    return {unique_repr(conjugacy_class(a)): sort(list(conjugacy_class(a))) for a in elem}.values()


def conjugacy_class(a):
    return {b for b in elem if is_conjugate(a, b)}


def is_conjugate(a, b):
    return any([reduce(g + a + inv(g)) == b for g in elem])


if __name__ == '__main__':
    H = ['e', 's', 'ttst', 'tstt']
    accum = []
    for l in quotient_group(H):
        accum += l
    print(accum)

    print(r'\begin{array}{r | cccccccccccc}' + '\n', end='')
    for a in accum:
        print(' & ' + a, end='')
    print("\\\\\n\\hline")
    for a in accum:
        print(a, end='')
        for b in accum:
            print(r' & ' + op(a, b), end='')
        print(r'\\')
    print(r'\end{array}')
