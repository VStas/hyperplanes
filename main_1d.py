__author__ = 'Stas'

import numpy as np

from graph import Graph

def build_graph(n, lmbd, mu):
    g = Graph()

    for i in range(0, n+1): # [0,1,2,...,n]
        g.add_vertex((i))

    #strelki s lambdami
    for i in range(0, n):
        g.add_arrow((i), (i+1), (n-i) * lmbd)

    #strelki s mu
    for i in range(n, 0, -1):
        g.add_arrow((i), (i-1), mu)

    return g

def build_equations(n, graph):

    matritsa_koefficientov = []

    for i in range(1, n+1): #ne berem pervoe uravnenie, vmesto nego p1 + .. + pn = 1
        equation = build_equation_for_vertex(i, n, graph)

        matritsa_koefficientov.append(equation)


    #[1,1,1,1...] eto p1 + p2 + p3 + ... = 1
    equation = [1] * (n+1)
    matritsa_koefficientov.append(equation)

    stolbets_svobodnih_chlenov = [0] * n + [1]

    return matritsa_koefficientov, stolbets_svobodnih_chlenov

def build_equation_for_vertex(i, n, graph):

    vertex = graph.get_vertex((i))
    incoming_arrows = vertex.incoming_arrows
    outcoming_arrows = vertex.outcoming_arrows

    equation = [0] * (n+1)
    k = 0 #tut summa vsego, chto vihodit iz vershini

    for arrow in outcoming_arrows:
        k += arrow[1]

    equation[i] = k

    for arrow in incoming_arrows:
        equation[arrow[0]] = -arrow[1]

    return equation


def main_1d(n, lmbd, mu):

    g = build_graph(n, lmbd, mu)
    matrix, stolbets = build_equations(n, g)

    matrix_numpy = np.array(matrix)
    stolbets_numpy = np.array(stolbets)

    result = np.linalg.solve(matrix_numpy, stolbets_numpy)
    print result

    #for i in range(0, n+1):
        #print g.get_vertex((i))
        #print g.get_vertex((i)).outcoming_arrows
        #print g.get_vertex((i)).incoming_arrows

main_1d(n=2, lmbd=2, mu=1)

# numpy example
#
# a = np.array([[3,1], [1,2]])
# b = np.array([9,8])
# x = np.linalg.solve(a, b)
# print x