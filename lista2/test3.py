from util import *


#funkcja generujaca dwa losowe wierzcholki do polaczenia
def add_edge(graph, capacity):
    i = randint(0, 19)
    j = randint(0, 19)
    while i == j or (i,j) in edg or (j,i) in edg:
        i = randint(0, 19)
        j = randint(0, 19)
        edg.append((i, j))
    graph.add_edge(i, j, a = 0, c = capacity)

#funkcja liczaca srednia przepustowosc wszystich krawedzi grafu
def avg_cap(graph):
    capacity = 0
    edges = 0
    for i in range(20):
        for edge in graph.edges(i, data = True):
            capacity += edge[2]["c"]
            edges += 1
    return capacity / edges

def test3(p, T_max, m, plot = False):
    graph = make_graph()
    matrix = make_matrix(20, 50)
    generate_flow(graph, matrix)
    generate_capacity(graph, matrix, m)

    capacity = avg_cap(graph)
    out = np.zeros(11)
    out[0] = calculate_reliability(graph, matrix, p, T_max, m)

    for i in range(10):
        add_edge(graph, capacity)
        out[i + 1] = calculate_reliability(graph, matrix, p, T_max, m)
    
    if plot:
        draw_plot(out)
    
    return out


def draw_plot(dane):
    plt.figure()

    plt.title("Wykres niezawodności od dodanych krawędzi")
    plt.xlabel("Liczba dodanych krawędzi")
    plt.ylabel("Niezawodność")

    plt.plot(np.linspace(0, 10, 11, True, dtype=int), dane, "b-o")

    plt.savefig("wykresy/test3.png", dpi=300)
    plt.close()