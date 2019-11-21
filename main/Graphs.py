from re import search


class Graph:
    _connectors = {'>', '-'}

    _vertices = {}
    _edges = {}

    def __init__(self):
        print("Empty Graph Made")

    @property
    def vertices(self):
        return self._vertices

    @vertices.setter
    def vertices(self, new_vertices):
        self._vertices = new_vertices

    def add_vertex(self, vertex):
        self._vertices += vertex

    def make_vertex(self):
        i = 0

        while i in self._vertices:
            i += 1

        self.add_vertex(i)

        return i

    @property
    def edges(self):
        return self._edges

    @edges.setter
    def edges(self, new_edges):
        self._edges = new_edges
        self.check_edges()

    def __sub__(self, other):
        self._vertices -= other
        self._edges -= other

    def __add__(self, other):
        pattern = self.connector_pattern()


    def check_edges(self):
        for str in self.edges:
            index = search(self.connector_pattern(), str).start()
            if index < 0:
                continue

            if str[:index] in self.edges and str[index + 1:] in self.edges:
                continue

            self._edges -= str

    def connector_pattern(self):
        pattern = r"{"

        for s in self._connectors:
            pattern += s + "|"

        pattern = pattern[:-1] + "}"
        print(pattern)
        return pattern

