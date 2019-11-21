import datetime


def make_dir(location):
    f1 = open(location, 'w')
    f1.write("# This is an automatically generated python file \n")
    f1.write("# generated on " + datetime.datetime.now().__str__() + ' \n\n')
    return f1


def make_tree(generators, elem, reduce_long):
    to_process, tree, elem_map = [0], ['e'], {'e': 0}
    length = len(generators)

    def calc_next_g(parent_index, g):
        return length * parent_index + g + 1

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
            next_pos = [calc_next_g(index, i) for i in range(length)]

            if isinstance(entry, int):
                # unreachable after int marked with -1 = 'e'
                for index in next_pos:
                    add_to_process_at(index, -1)
            else:
                for subi in range(len(next_pos)):
                    index = next_pos[subi]
                    next_str = validate_str(entry + generators[subi], index)
                    add_to_process_at(index, next_str)

        return next_process

    while len(elem_map) < len(elem):
        to_process = process(to_process)

    process(to_process)

    return tree


def clean_reduction_map(reduction_map):
    reduction_map = {k: v for k, v in reduction_map.items() if k is not v}

    priority_list = [(len(k) - len(v), k, v) for k, v in reduction_map.items()]
    reduction_map.clear()
    priority_list.sort(key=lambda i: -i[0])
    return {k: v for _, k, v in priority_list}


def make_reduction_map(reduction_map, generators, elem):
    reduction_map['ee'] = 'e'

    for g in generators:
        reduction_map[g + 'e'] = g
        reduction_map['e' + g] = g

    if 'e' not in elem:
        elem.insert(0, 'e')

    def reduce_long(raw):
        entry = raw.replace('e', '')

        if len(entry) == 0:
            return 'e', True

        if entry in elem:
            return entry, True

        for _ in range(len(raw) + 1):
            for target, repl in reduction_map.items():
                entry = entry.replace(target, repl)

            if entry in elem:
                return entry, True

        return raw, False

    print("In the following lines, you will be prompted to simplify expressions. ")
    print("If the expression does not simplify, simply hit enter. ")
    for a in elem:
        for b in elem:
            if 'e' is a or 'e' is b:
                continue

            key = a + b

            if key in reduction_map:
                continue

            value, success = reduce_long(key)

            if not success:
                text = input(key + ": ")
                if len(text.strip()) > 0:
                    elem.append(value)
                    continue

            if value not in elem:
                elem.append(value)

            reduction_map[key] = value

    return elem, clean_reduction_map(reduction_map)


def make_reduce(generators):
    tab = '    '
    ltab = '\n' + tab
    file.write("def reduce(raw):\n")
    file.write(tab + """if len(raw) > 400:
        return reduce_long(raw)\n""")

    file.write(ltab + "last_pos = 0")
    file.write(ltab + "last_entry = 'e'\n\n")

    file.write("""    for char in raw:
        if char is 'e':
            continue\n""")

    length = len(generators)
    for i in range(1, length):
        file.write(tab*2 + """elif char is '""" + generators[i - 1] + """':
            next_pos = 2 * last_pos + """ + str(i) + '\n')
    file.write(tab*2 + """else:
            next_pos = 2 * last_pos + """ + str(length) + '\n')
    file.write(tab * 2 + """next_entry = rainbow_tree[next_pos]
        if isinstance(next_entry, int):
            last_pos = next_entry
            last_entry = rainbow_tree[next_entry]
        else:
            last_pos = next_pos
            last_entry = next_entry

    return last_entry""")


def make_group():
    # get generators
    generators = ['e']
    while 'e' in generators:
        print("Input all generators, separated by spaces: ", end="")
        generators = input().split()
        if 'e' in generators:
            print('\'e\' is a reserved as the identity element, please rename')

    file.write("# Generator list\n")
    file.write("generators = " + str(generators) + '\n\n')

    # get rules
    print("Input the basic rules <target> = <simplification> followed by enter (blank to stop): ")
    reduction_map = {}
    for line in iter(input, ''):
        left, right = line[:line.index('=')], line[line.index('=') + 1:]
        left, right = left.strip(), right.strip()
        reduction_map[left] = right

    # make table/elem
    elem = generators.copy()

    elem, reduction_map = make_reduction_map(reduction_map, generators, elem)

    file.write("# group element list\n")
    file.write("elem = " + str(elem) + '\n\n')

    file.write("# long_reduce reduction map\n")
    file.write("reduction_map = " + format_dict_to_fit(reduction_map, ", ", mid_line_leader='                 ')+'\n\n')

    file.write("""# use only when len(raw) > 500. Otherwise substantially slower than reduce
def reduce_long(raw):
    entry = raw

    for _ in range(len(raw)):
        for target, repl in reduction_map.items():
            entry = entry.replace(target, repl)

        if entry in elem:
            break

    return entry\n\n\n""")

    def reduce_long(raw):
        entry = raw

        for _ in range(len(raw)):
            for target, repl in reduction_map.items():
                entry = entry.replace(target, repl)

            if entry in elem:
                break

        return entry

    tree = make_tree(generators, elem, reduce_long)

    file.write("rainbow_tree = " + format_list_to_fit(tree, h_chars=100, mid_line_leader='                ') + '\n\n\n')

    make_reduce(generators)

    return elem, reduction_map


def make_basic_group(group_type):
    n = int(input("What is n: "))
    group_str = group_type + "_" + str(n)
    file.write("# This is a " + group_str + " group \n")
    file.write("n = " + str(n) + "\n\n")

    elem = list(range(1, n))
    if group_type == 'U':
        for i in range(2, n):
            if n % i == 0:
                for r in range(i, n, i):
                    if r in elem:
                        elem.remove(r)
    file.write("# The element list of " + group_str + ' \n')
    file.write("elem = " + str(elem) + "\n\n")

    if group_type == 'Z':
        def op(x, y):
            return (x + y) % n

        file.write("\n# The standard operation for Z_n \n")
        file.write("""def op(x, y):
    return (x + y) % n\n\n\n""")
    else:
        def op(x, y):
            return (x * y) % n

        file.write("\n# The standard operation for " + group_str + "\n")
        file.write("""def op(x, y):
    return (x * y) % n\n\n\n""")

    file.write("# The standard Cayley Table making function for " + group_str + " in dictionary form \n")
    file.write("""def make_table(elem, op):
    out = {}
    for a in elem:
        for b in elem:
            out[(a, b)] = op(a, b)
    return out\n\n\n""")

    cayley = make_table(elem, op)
    file.write("# The Cayley table for " + group_str + '\n')
    file.write("table = " + format_dict_to_fit(cayley, mid_line_leader='         '))

    return 0, elem, cayley


def make_z_group():
    return make_basic_group('Z')


def make_u_group():
    return make_basic_group('U')


def get_type(file):
    user = ''
    options = ['Zn', 'Un', 'other']

    while user not in options:
        user = input("Zn, Un, or other: ").strip(' ')
        if user not in options:
            print('Please type Zn, Un, or other')

    return options.index(user)


def make_table(elem, op):
    table = {}
    for a in elem:
        for b in elem:
            table[(a, b)] = op(a, b)
    return table


def surround(s):
    if isinstance(s, str):
        return '\"' + s + '\"'
    else:
        return str(s)


def format_list_to_fit(list, joiner=", ", h_chars=110, use_braces=True, mid_line_leader=""):
    parser = lambda item: surround(item) + joiner
    return format_obj_to_fit(list, joiner, parser, list, h_chars, use_braces, mid_line_leader)


def format_dict_to_fit(map, joiner=", ", h_chars=110, use_braces=True, mid_line_leader=""):
    parser = lambda item: surround(item[0]) + ": " + surround(item[1]) + joiner
    return format_obj_to_fit(map, joiner, parser, map.items(), h_chars, use_braces, mid_line_leader)


def format_obj_to_fit(obj, joiner, parser, iterator, h_chars, use_braces, mid_line_leader):
    out = """"""
    if use_braces:
        out += '{'
    line_counter = len(out)
    for item in iterator:
        item_str = parser(item)
        length = len(item_str)

        if line_counter + length - 1 > h_chars and line_counter > 0:
            out += """\n""" + mid_line_leader
            line_counter = len(mid_line_leader)

        out += item_str
        line_counter += length

    out = out[:-len(joiner)]

    if use_braces:
        out += '}'

    return out


def add_universal_functions(file, elem):
    file.write("""\n\ndef latex_cayley():
    str = "\\\\[\\\\begin{array}{ l | """ + "".join(['c' for _ in elem]) + """ }\\n & "
    str += " & ".join([x.__str__() for x in elem]) + "\\\\\\\\\\n" 
    str += "\\\\hline \\n" 
    for e in elem:
        str += e.__str__() + " & " + " & ".join([table[e, x].__str__() for x in elem]) + " \\\\\\\\\\n"
    str += "\\\\end{array}\\\\]"
    return str\n""")


if __name__ == '__main__':
    file = make_dir(input('File name: ') + '.py')

    type = get_type(file)

    if type == 0:
        i, elem, table = make_z_group()
    elif type == 1:
        i, elem, table = make_u_group()
    else:
        elem, table = make_group()

    add_universal_functions(file, elem)

    file.write('\n')
