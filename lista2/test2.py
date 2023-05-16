from util import *

#funkcja zwiekszajaca przepustowosci krawedzi
def increase_capacity(graph, mul, i):
    for i in range(20):
        for edge in graph.edges(i, data = True):
            edge[2]["c"] = edge[2]["c"] / (1 + (i * mul)) * (1 + (mul * (i + 1)))

def test2(p, T_max, m, mul, plot = False):
    graph = make_graph()
    matrix = make_matrix(20, 50)
    generate_flow(graph, matrix)
    generate_capacity(graph, matrix, m//16)

    out = np.zeros(11)
    dane = np.zeros(11)

    out[0] = (calculate_reliability(graph, matrix, p, T_max, m))
    dane[0] = 1

    for i in range(10):
        increase_capacity(graph, mul, i)
        out[i + 1] = calculate_reliability(graph, matrix, p, T_max, m)
        dane[i + 1] = dane[0] * (1 + (i + 1) * mul)
    
    if plot:
        draw_plot(dane, out)

    return out

def draw_plot(dane, wyniki):
    plt.figure()

    plt.title("Wykres niezawodności od przepustowości")
    plt.xlabel("Przepustowość zwiękoszona x razy")
    plt.ylabel("Niezawodność")

    plt.plot(dane, wyniki, "b-o")

    plt.savefig("wykresy/test2.png", dpi=300)
    plt.close()