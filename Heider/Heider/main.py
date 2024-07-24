import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import itertools


# 65:35 daje większe prawdopodobieństwo na pojawienie się stanu raju, a im więcej 1 (podane wyższe prab), tym jeszcze większe
def create_complete_graph(N, prob=0.5):
    '''
    Funkcja tworzy graf zupełny z krawędziami -1 i 1 z podanym rozkładem prawdopodobieństwa wag.
    N: liczba wierzchołków
    prob: prawdopodobieństwo wystąpienia wagi = 1, default 50:50
    Zwraca utworzony graf.
    '''
    G = nx.complete_graph(N)

    # wszystkie krawędzie
    edges = list(G.edges())
    
    weights = [1, -1]
    probabs = [prob, 1 - prob]
    
    # wylosuj wagi dla wszystkich krawędzi
    chosen_weights = np.random.choice(weights, size=len(edges), p=probabs)

    # połącz wagę z krawędzią
    for edge, weight in zip(edges, chosen_weights):
        i, j = edge
        G[i][j]['weight'] = weight
    
    return G


def update_edges_weight_sync(G):
    '''
    Funkcja zmienia niezbalansowane trójkąty w układzie na zbalansowane (synchronicznie).
    G: utworzony graf
    '''
    edges = list(G.edges())
    # nowe wagi krawędzi do zapamiętania
    new_weights = {}
    for i, j in edges:
        # suma iloczynów krawędzi trójkątów połączonych z aktualnie badaną krawędzią i, j (nie uwzględniamy jej)
        triangle_sum = 0
        
        # sąsiedzi wierzchołka i oraz j
        i_neighbors = set(G.neighbors(i))
        j_neighbors = set(G.neighbors(j))
        # wspólnie sąsiedzi wierzchołków i oraz j
        common_neighbors = i_neighbors.intersection(j_neighbors)
        
        # dla każdego wierzchołka tworzącego trójkąt z krawędzią i, j
        for k in common_neighbors:
            if k != i and k != j:
                product = G.edges[i, k]['weight'] * G.edges[j, k]['weight']
                triangle_sum += product

        # jeśli suma > 0 znak dodatni, jeśli suma < 0 znak ujemny, w przypadku 0 nie modyfikuj
        if triangle_sum != 0:
            # zapamiętaj nową wagę krawędzi
            new_weights[(i, j)] = 1 if triangle_sum > 0 else -1
            
    # zaktualizuj wszystkie wagi krawędzi do aktualnie zapamiętanych
    for (i, j), weight in new_weights.items():
        G.edges[i, j]['weight'] = weight
      

def update_edges_weight_async(G):
    '''
    Funkcja zmienia niezbalansowane trójkąty w układzie na zbalansowane (asynchronicznie).
    G: utworzony graf
    '''
    edges = list(G.edges())
    for i, j in edges:
        # suma iloczynów krawędzi trójkątów połączonych z aktualnie badaną krawędzią i, j (nie uwzględniamy jej)
        triangle_sum = 0
        
        # sąsiedzi wierzchołka i oraz j
        i_neighbors = set(G.neighbors(i))
        j_neighbors = set(G.neighbors(j))
        # wspólnie sąsiedzi wierzchołków i oraz j
        common_neighbors = i_neighbors.intersection(j_neighbors)
        
        # dla każdego wierzchołka tworzącego trójkąt z krawędzią i, j
        for k in common_neighbors:
            if k != i and k != j:
                product = G.edges[i, k]['weight'] * G.edges[j, k]['weight']
                triangle_sum += product

        # jeśli suma > 0 znak dodatni, jeśli suma < 0 znak ujemny, w przypadku 0 nie modyfikuj
        if triangle_sum != 0:
            # zmień wagę aktualnej krawędzi
            G.edges[i, j]['weight'] = 1 if triangle_sum > 0 else -1


def calculate_U(G):
    '''
    Funkcja oblicza, czy wszystkie trójkąty w sieci są zbalansowane (U).
    G: utworzony graf
    Zwraca wynik obliczeń (U).
    '''
    # sumy iloczynów krawędzi tworzących trójkąty
    edges_mult_sum = 0
    # ile można utworzyć trójkątów w grafie
    triangles_num = 0
    U = 0
    for i, j, k in itertools.combinations(G.nodes(), 3):
        # jeśli trzy wierzchołki są połączone ze sobą krawędziami
        if G.has_edge(i, j) and G.has_edge(j, k) and G.has_edge(k, i):
            triangles_num += 1
            edges_mult_sum += G.edges[i, j]['weight'] * G.edges[j, k]['weight'] * G.edges[k, i]['weight']
    U = -1 * (edges_mult_sum / triangles_num)
    
    return U


def calculate_avg_weight(G):
    '''
    Funkcja oblicza średni znak krawędzi uśredniony po wszystkich krawędziach.
    G: utworzony graf
    Zwraca obliczoną średnią.
    '''
    # "zbierz" znaki ze wszystkich krawędzi
    signs = [G.edges[i, j]['weight'] for i, j in G.edges()]
    
    return np.mean(signs)


def draw_graph(G, name='graf'):
    '''
    Funkcja rysuje graf.
    G: utworzony graf
    name: nazwa zapisywanej grafiki
    '''
    # oblicz pozycje elementów na grafie (wizualnie je rozdziel)
    pos = nx.spring_layout(G)
    edges = G.edges(data=True)
    edge_colors = ['green' if edge[2]['weight'] == 1 else 'red' for edge in edges]
    nx.draw(G, pos, edge_color=edge_colors, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
    plt.savefig(f'{name}.png')
    plt.show()


def print_edges_weight(G):
    '''
    Funkcja wypisuje wierzchołki i wagę łączącej je krawędzi.
    G: utworzony graf
    '''
    for i, j, data in G.edges(data=True):
        print(i, j, data['weight'])
        f.write(f"{i}, {j}, {data['weight']}\n")


def print_graph_data(t, U, avg_xij):
    '''
    Funkcja wypisuje dane o grafie.
    t: krok symulacji
    U: wartość oznaczająca, czy wszystkie trójkąty w sieci są zbalansowane
    avg_xij: średni znak krawędzi uśredniony po wszystkich krawędziach
    '''
    print("t, U, avg_xij:", end=' ')
    print(t, U, avg_xij)
    f.write(f"t, U, avg_xij: {t}, {U}, {avg_xij}\n")



# plik do zapisywania rezultatów
f = open('heider_wynik.txt', 'w')

# liczba wierzchołków
N = 50

# krok czasowy
t = 0

# czy wszystkie trójkąty (triady relacji) w grafie zbalansowane
U = float('inf')
U_prev = float('inf')
# średni znak wszystkich krawędzi w układzie
avg_xij = float('inf')
avg_xij_prev = float('inf')

# stwórz graf
# -- !! --
G = create_complete_graph(N)
# G = create_complete_graph(N, 0.65)

# rysuj początkowy graf
draw_graph(G, 'graf_init')

# oblicz początkowe wartości dla grafu
U = calculate_U(G)
avg_xij = calculate_avg_weight(G)
    
while True:
    print_graph_data(t, U, avg_xij)
    
    # jeśli graf już na początku jest zrównoważony
    if t == 0 and U == -1:
        print('Graf zrównoważony')
        f.write('Graf zrównoważony\n')
        break
        
    # -- !! --
    update_edges_weight_sync(G)
    # update_edges_weight_async(G)
    
    U = calculate_U(G)
    avg_xij = calculate_avg_weight(G)
    
    t += 1
    
    if U == U_prev and avg_xij == avg_xij_prev:
        break
    
    U_prev = U
    avg_xij_prev = avg_xij
    
# rysuj końcowy graf
draw_graph(G, 'graf_fin')

# wypisz trójki: wierzchołki i, j oraz wartość ich krawędzi xij
print('i, j, xij:')
f.write("\ni, j, xij:\n")
print_edges_weight(G)
f.write('\n')

# sprawdź wynik równoważenia sieci
if U == -1 and avg_xij == 1:
    print('Stan raju')
    f.write('Stan raju')
elif U == -1 and avg_xij != 1:
    print('Grupy: wzajemnie wrogie, wewnętrznie zaprzyjaźnione')
    f.write('Grupy: wzajemnie wrogie, wewnętrznie zaprzyjaźnione')

f.close()
