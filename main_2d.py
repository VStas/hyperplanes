__author__ = 'Stas'

import numpy as np

from graph import Graph
from jinja2 import Environment, FileSystemLoader
import os

# Capture our current directory
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                        trim_blocks=True)

# n1 = 2, n2 = 3
#
# (0 0) (1 0) (2 0)
# (0 1) (1 1) (2 1)
# (0 2) (1 2) (2 2)
# (0 3) (1 3) (2 3)

def build_graph(n1, n2, lmbd, mu):
    g = Graph()

    for i in range(0, n1 + 1):
        for j in range(0, n2 + 1):
            g.add_vertex((i, j))


    #strelki s lambdami i mu po gorizontali
    for j in range(0, n2 + 1):      # 0 <= j <= n2
        for i in range(0, n1):      # 0 <= i <= n1-1
            g.add_arrow( (i,j) ,      (i+1,j) ,    (n1 - i) * lmbd )    #strelka s lambda
            g.add_arrow( (i+1,j) ,    (i,j) ,      mu              )    #strelka s mu v druguu storonu

    #strelki s lambdami po vertikali
    for i in range(0, n1 + 1):
        for j in range(0, n2):
            g.add_arrow((i,j), (i,j+1), (n2 - j) * lmbd)


    #strelki s mu v pervom stolbtse (t k u nas tolko odin OA)
    for j in range(0, n2):
        g.add_arrow((0, j+1), (0, j), mu)

    return g


def build_equations(n1, n2, graph):
    matritsa_koefficientov = []

    for i in range(0, n1+1):
        for j in range(0, n2+1):
            equation = build_equation_for_vertex(i, j, n1, n2, graph)

            matritsa_koefficientov.append(equation)

    equation = [1] * (n1 + 1) * (n2 + 1)
    matritsa_koefficientov[0] = equation

    stolbets_svobodnih_chlenov = [0] * (n1 + 1) * (n2 + 1)
    stolbets_svobodnih_chlenov[0] = 1

    return matritsa_koefficientov, stolbets_svobodnih_chlenov



def get_var_index(i, j, n1, n2):
    return i * (n2 + 1) + j

def build_equation_for_vertex(i, j, n1, n2, graph):
    vertex = graph.get_vertex((i, j))
    incoming_arrows = vertex.incoming_arrows
    outcoming_arrows = vertex.outcoming_arrows

    equation = [0] * (n1 + 1) * (n2 + 1)
    k = 0 #tut summa vsego, chto vihodit iz vershini

    for arrow in outcoming_arrows:
        k += arrow[1]

    equation[get_var_index(i,j, n1, n2)] = k

    for arrow in incoming_arrows:
        from_vertex = arrow[0]
        arrow_value = arrow[1]

        from_i, from_j = from_vertex
        equation[get_var_index(from_i, from_j, n1, n2)] = -arrow_value

    return equation

def get_graph_dimentions(graph):
    # get graph dimentions by finding the maximum indices 
    # of nodes (assuming that the representing matrix is rectangular)
    v = graph.get_vertices()
    return (max([x[0] for x in v]), max(x[1] for x in v))

def output_graph(graph, name="out.gv"):
    graph_output = j2_env.get_template('template.gv').render(graph=graph, dimentions=get_graph_dimentions(graph))
    with open("out.gv", "wb") as fh:
        fh.write(graph_output)


def main_2d(n1, n2, lmbd, mu, output_graphname="out.gv"):

    g = build_graph(n1, n2, lmbd, mu)

    matrix, stolbets = build_equations(n1, n2, g)

    # for row in matrix:
    #     print row

    # print '-----'
    # print stolbets
    # print '-----'

    matrix_numpy = np.array(matrix)
    stolbets_numpy = np.array(stolbets)

    result = np.linalg.solve(matrix_numpy, stolbets_numpy)
    print (result, g.get_vertices())

    output_graph(g, output_graphname)
    print "Graph was successfully printed to " + output_graphname
    return g

    #
    # for i in range(0, n1+1):
    #         for j in range(0, n2+1):
    #             print g.get_vertex((i,j))
    #             print g.get_vertex((i,j)).outcoming_arrows
    #             print g.get_vertex((i,j)).incoming_arrows

g = main_2d(n1=2, n2=3, lmbd=2, mu=1)