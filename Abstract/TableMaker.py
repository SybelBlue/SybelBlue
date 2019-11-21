from Abstract.GroupST import *
from random import choice
import time


def make_test(n):
    return ''.join([choice(elem[1:]) for _ in range(n)])


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


def format_dict_to_fit(map, joiner, h_chars, use_braces=True):
    out = """"""
    if use_braces:
        out += '{'
    line_counter = len(out)
    for item in map.items():
        item_str = '\"' + item[0] + "\": \"" + item[1] + '\"' + joiner
        length = len(item_str)

        if line_counter + length - 1 > h_chars and line_counter > 0:
            out += """\n"""
            line_counter = 0

        out += item_str
        line_counter += length

    out = out[:-len(joiner)]

    if use_braces:
        out += '}'

    return out


def current_milli_time():
    return int(round(time.time() * 1000))


def make_rainbow_tree(parent):
    to_process, tree, elem_map = [0], [parent], {parent: 0}

    def calc_next_s(parent_index):
        return 2 * parent_index + 1

    def calc_next_t(parent_index):
        return 2 * parent_index + 2

    def validate_str(raw, value_index):
        val = reduce_long(raw)
        if val in elem_map:
            return elem_map[val]
        else:
            elem_map[val] = value_index
            return val

    def process(items):
        next_process = []

        def add_to_process_at(value_index, value):
            tree.insert(value_index, value)
            next_process.append(value_index)

        for index in items:
            entry = tree[index]
            next_s = calc_next_s(index)
            next_t = calc_next_t(index)

            if type(entry) is int:
                # unreachable after int marked with -1 = 'e'
                add_to_process_at(next_s, -1)
                add_to_process_at(next_t, -1)
            else:
                next_s_str = validate_str(entry + 's', next_s)
                add_to_process_at(next_s, next_s_str)

                next_t_str = validate_str(entry + 't', next_t)
                add_to_process_at(next_t, next_t_str)

        return next_process

    while len(elem_map) < len(elem):
        to_process = process(to_process)

    process(to_process)

    return tree


# at length 500, reduce_long out performs reduce on average.
def compare_reduce_speeds():
    reduce_times, reduce_long_times = [], []
    for i in range(1, 50):
        raws = [make_test(i + 500) for _ in range(500)]
        avg_len = mean([len(raw) for raw in raws])
        t = current_milli_time()
        [reduce(raw) for raw in raws]
        reduce_times.append((current_milli_time() - t) / avg_len)

        raws = [make_test(i + 500) for _ in range(500)]
        avg_len = mean([len(raw) for raw in raws])
        t = current_milli_time()
        [reduce_long(raw) for raw in raws]
        reduce_long_times.append((current_milli_time() - t) / avg_len)

    print()
    print(mean(reduce_times), ": ", reduce_times)
    print(mean(reduce_long_times), ": ", reduce_long_times)
    gap = [x - y for x, y in zip(reduce_long_times, reduce_times)]
    print(mean(gap), ": ", gap)
