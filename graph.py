__author__ = 'Stas'

class Vertex:
    def __init__(self, node):
        self.node = node
        self.incoming_arrows = []
        self.outcoming_arrows = []

    def __str__(self):
        return str(self.node)

    def __repr__(self):
        return str(self.node)

class Graph:
    def __init__(self):
        self.vertex_dict = {}

    def add_vertex(self, node):
        new_vertex = Vertex(node)
        self.vertex_dict[node] = new_vertex
        return new_vertex

    def add_arrow(self, fr, to, value):
        self.get_vertex(fr).outcoming_arrows.append((to, value))
        self.get_vertex(to).incoming_arrows.append((fr, value))

    def get_vertices(self):
        return self.vertex_dict.keys()

    def get_vertex(self, node):
        if node in self.vertex_dict:
            return self.vertex_dict[node]
        else:
            return None
