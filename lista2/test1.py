from util import *

def increase(matrix, increment):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] += increment

def test1(p, T_max, m, plot = False):
    graph = make_graph()
    matrix = make_matrix(20, 5)
    generate_flow(graph, matrix)
    generate_capacity(graph, matrix, m)

    out = np.zeros(11)
    out[0] = (calculate_reliability(graph, matrix, p, T_max, m))

    for i in range(10):
        increase(matrix, 7)
        out[i + 1] = calculate_reliability(graph, matrix, p, T_max, m)
    
    if plot:
        draw_plot(out)

    return out

def draw_plot(dane):
    plt.figure()

    plt.title("Wykres niezawodności od wartości natężeń")
    plt.xlabel("Natężenia należą do zakresu [0, x]")
    plt.ylabel("Niezawodność")

    plt.plot(np.linspace(5, 5 + 10 * 7, 11, True), dane, "b-o")

    plt.savefig("wykresy/test1.png", dpi=300)
    plt.close()