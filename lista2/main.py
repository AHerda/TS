from util import *
from test1 import test1
from test2 import test2
from test3 import test3

n = 20

def main():
    #graph = make_graph()
    #matrix = make_matrix(n, 5)
    #generate_capacity(graph, matrix, 8)
    #generate_flow(graph, matrix)
    """draw_graph(graph)
    print(matrix)
    print(calculate_reliability(graph, matrix, 0.9, 0.2, 128))"""

    #print(test1(0.8, 0.1, 128, True))
    #print(test2(0.8, 0.1, 128, 0.1, True))
    print(test3(0.8, 0.1, 128, True))

if __name__ == "__main__":
    main()