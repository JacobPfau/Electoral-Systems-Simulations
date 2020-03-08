import numpy as numpy

class Vertex():
    '''
    A vertex within a directed graph.
    '''
    def __init__(self, name=None):
        self.out_vertices = []
        self.in_vertices = []
        self.name = name


class NamedGraph():
    '''
    A directed gaph in which the vertices are named
    '''
    def __init__(self, vertices=None,):
        self.vertices = vertices

    def add_edge(self, source_name, target_name):
        self.vertices[source_name].out_vertices.append(self.vertices[target_name])
        self.vertices[target_name].in_vertices.append(self.vertices[source_name])

def find_cycle(upstream_vertices, target, max_depth, depth=0,):
    '''
    Recursively performs DFS up to given depth to determine whether adding edges from initially passed upstream vertices to target will result in a cycle
    '''
    if not upstream_vertices:
        return False
    if target in upstream_vertices:
        return True
    elif depth<max_depth:
        for vertex in upstream_vertices:
            if find_cycle(vertex.in_vertices, target, max_depth, depth=depth+1): return True
        return False
    else:
        return False