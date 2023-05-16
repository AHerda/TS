import networkx as nx
import matplotlib.pyplot as plt
from random import randint, uniform
import numpy as np

edg = []

#funckja generujaca dodecahedron
def make_graph(v = 20):
    G = nx.Graph()
    G.add_nodes_from(list(range(v)))
    
    edges_temp = []
    for i in range(v - 1):
        edges_temp.append((i, i + 1))
    edges_temp.extend(((0, 4), (14, 5), (15, 19)))
    edges_temp.remove((4, 5))
    edges_temp.remove((14, 15))

    i = 0
    j = 5
    while i<5:
        edges_temp.append((i,j))
        edges_temp.append((i+15, j+1))
        i += 1
        j += 2
    for i, j in edges_temp:
        G.add_edge(i, j, a = 0, c = 0)
    
    global edg
    edg = edges_temp
    
    return G

#funkcja tworzy wizualizacje grafu
def draw_graph(graph):
    plt.figure(figsize=(8, 8))
    plt.title("Wzór grafu")
    pos = nx.shell_layout(graph, (list(range(5)), list(range(5, 15)), list(range(15, 20))), .4)
    #pos = nx.spring_layout(graph)
    nx.draw_networkx_labels(graph, pos, font_color="w")
    #nx.draw_networkx_edge_labels(graph, pos, font_size=6, font_color="r", bbox=dict(fc = "w", linewidth = 0, alpha=1.0))
    nx.draw(graph, pos)
    plt.savefig("lista22/wykresy/Graf.png", dpi=400)

#funkcja generujaca macierz natezen o maksymalnej liczbie wysylanych pakietow max
def make_matrix(v, max):
    matrix = np.zeros((v, v), dtype=int)
    for i in range(v):
        for j in range(v):
            if i == j:
                matrix[i][j] = 0
            else:
                matrix[i][j] = randint(0, max)
    return matrix

#funkcja generujaca przeplyw, wraca true jezeli z kazdego wierzcholka mozna wszedzie wyslac okreslona w macierzy natezen liczbe pakietow
def generate_flow(graph, matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] != 0:
                path = generate_path(graph, i, j, matrix[i][j])
                if len(path) == 0:
                    return False
                for k in range(0, len(path)-1):
                    graph[path[k]][path[k+1]]["a"] += matrix[i][j]
    return True

#funkcja generujaca przepustowosc sieci
def generate_capacity(graph, matrix, m):
    for i in range(len(matrix)):
        max_size = max(matrix[i])
        for edge in graph.edges(i, data = True):
            edge[2]["c"] = int(max_size * len(matrix)**2 * m * uniform(2.0, 3.0))

#funkcja generujaca sciezke package pakietow z wierzcholka i do j
def generate_path(graph, i, j, package):
    try:
        path = nx.dijkstra_path(graph, i,  j)
    except:
        return []
    if_ok = False
    gen = nx.all_simple_paths(graph, source = i, target = j)
    while not if_ok:
        if_ok = True
        for k in range(0, len(path)-1):
            if graph[path[k]][path[k+1]]["a"] + package > graph[path[k]][path[k+1]]["c"]:
                if_ok = False
                try:
                    path = next(gen)
                except:
                    path = []
                break
    return path

#funkcja liczaca opoznienie pakietow wedlug wzoru z polecenia
def calculate_delay(graph, matrix, m):
    G = 0
    for row in matrix:
        for num in row:
            G += num
    sum_e = 0
    for i in range(len(matrix)):
        for edge in graph.edges(i, data = True):
            term = edge[2]["a"]/(edge[2]["c"]/m-edge[2]["a"]) #liczenie wyrazenia dla kazdej krawedzi
            if term < 0: #jezeli wyszlo ujemne to znaczy, ze krawedz zostala przeciazona i nalezy wrocic fail
                return -1
            else:
                sum_e += term
    return sum_e / G

#funkcja liczace miare niezawodnosci sieci
def calculate_reliability(graph, matrix, p, T_max, m, iterations=200, intervals=5):
    counter = 0
    for i in range(iterations):
        graph_temp = graph.copy()
        for j in range(intervals):
            to_del = []

            for edge in graph_temp.edges:
                i = uniform(0.0,1.0)
                if i > p:
                    to_del.append(edge)
        
            for edge in to_del:
                graph_temp.remove_edge(*edge)
            
            connected = generate_flow(graph_temp, matrix)

            if connected:
                T = calculate_delay(graph_temp, matrix, m)
                if T < T_max and T > 0: 
                    counter += 1
            else:
                break
    return counter / (iterations * intervals)