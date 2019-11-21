def read_file(file):
    with open(file, 'r') as text:
        print(file + " loaded...")
        return [x.replace('\n', '').split(' ') for x in text.readlines()]


def parse_file(lines):
    for line in lines:
        parse_cmd(line)


def add_node(node):
    if node not in graph[0]:
        graph[0] += node


def add_undirected(edge):
    add_edge(edge)
    add_edge(edge[::-1])


def add_edge(edge):
    [add_node(item) for item in edge]
    if edge not in graph[1]:
        graph[1] += [edge]


def remove_node(node):
    graph[0] -= node


def remove_edge(edge):
    graph[1] -= edge


graph = [[], []]


def neighbors(start):
    return [x[1] for x in graph[1] if x[0] == start]


def find_cycle():
    path = set()
    path_list = []

    def visit(vertex):
        path.add(vertex)
        for neighbour in neighbors(vertex):
            if neighbour in path or visit(neighbour):
                if path not in path_list:
                    return True
        path.remove(vertex)
        return False

    while any(visit(v) for v in graph[0]):
        path_list += [path]
        path = set()

    return not not len(path_list), path_list


def in_degree(node):
    return len([x for x in graph[1] if x[1] == node])


def out_degree(node):
    return len([x for x in graph[1] if x[0] == node])


def degree_map():
    return {node: (in_degree(node), out_degree(node)) for node in graph[0]}


def check():
    if len(graph[0]) > 0:
        print(find_cycle())
        print(degree_map())


def parse_cmd(cmd):
    i = 0
    while i < len(cmd):
        # block, args = None, None
        if cmd[i] == "load":
            i += 1
            lines = read_file(cmd[i])
            parse_file(lines)
        elif cmd[i] == 'node':
            i += 1
            add_node(cmd[i])
        elif cmd[i] == '->':
            i += 1
            add_edge((cmd[i - 2], cmd[i]))
        elif cmd[i] == '<-':
            i += 1
            add_edge((cmd[i], cmd[i - 2]))
        elif cmd[i] == '<->':
            i += 1
            add_undirected((cmd[i - 2], cmd[i]))
        elif cmd[i] == 'edge':
            directed = 'directed' in cmd
            if directed:
                if cmd.index('directed') < i:
                    i -= 1
                cmd.remove('directed')
            i += 2
            edge = (cmd[i - 1], cmd[i])
            if directed:
                add_edge(edge)
            else:
                add_undirected(edge)
        elif cmd[i] == 'check':
            check()

        i += 1


if __name__ == '__main__':
    # parse_file(read_file('temp.txt')); print(graph)
    cmd = input("> ").split()
    while "stop" not in cmd:
        parse_cmd(cmd)
        print(graph)
        cmd = input("> ").split(' ')