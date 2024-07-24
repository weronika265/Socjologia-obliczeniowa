import numpy as np
import matplotlib.pyplot as plt
import random


def init_rand_arr_2d(L, p, K):
    '''
    Funkcja tworzy sieć 2D z aktorami posiadającymi cząstki wiedzy o określonym prawdopodobieństwie.
    L: wymiar sieci
    p: prawdopodobieństwo posiadania cząstki wiedzy
    K: liczba dostępnym cząstek wiedzy u każdego aktora
    Zwraca utworzoną sieć.
    '''
    # stwórz sieć o okreśłonych wymiarach
    rand_arr_2d = np.empty((L, L), dtype=object)
    
    for i in range(L):
        for j in range(L):
            k_lst = []
            for _ in range(K):
                # dla każdego aktora losuj posiadanie czątki z określonym prawdopodobieństwem
                rand_k = random.choices([1, 0], weights=[p, 1-p])[0]
                k_lst.append(rand_k)
            rand_arr_2d[i, j] = k_lst
        
    return rand_arr_2d


def count_full_and_half_knowledge(arr_2d, K):
    '''
    Funkcja oblicza, ilu aktualnie aktorów ma całość wiedzy (K) i połowę wiedzy (K/2).
    arr_2d: aktualny stan sieci
    K: liczba dostępnych cząstek wiedzy
    Zwraca aktorów z pełną wiedzą (K) i połową wiedzy (K/2).
    '''
    count_K = 0
    count_K_half = 0
    
    # dla każdego aktora w sieci
    for row in arr_2d:
        for actor in row:
            k_count = actor.count(1)
            # jeśli aktor posiada wszystkie cząstki wiedzy
            if k_count == K:
                count_K += 1
            # jeśli aktor posiada połowę cząstek wiedzy
            elif k_count == K / 2:
                count_K_half += 1
                
    return count_K, count_K_half



# stwórz i otwórz plik do zapisu rezultatów
f = open('wynik.txt', 'w')

# rozmiar sieci
L = 5

# liczba cząstek wiedzy w organizacji dla każdego aktora
K = 4

# prawdopodobieństwa na wylosowanie posiadania cząstki wiedzy
probabs = [0.9, 0.7, 0.5, 0.3]

# liczba symulacji (dla każdego prawdopodobieństwa)
R = 50

# rezultaty wszystkich symulacji dla wszystkich prawdopodobieństw
results = []
    
# symulacja dla wybranego prawdopodobieństwa
for p in probabs:
    f.write(f'-- Prawdopodobieństwo {p} --\n')
    # wyniki K i K/2 dla wszystkich 50 symulacji dla konkretnego prawdopodobieństwa
    simulations = []
    # odbycie R symulacji dla wybranego prawdopodobieństwa
    for _ in range(R):
        f.write(f'Symulacja #{_ + 1}:\n')
        # stan sieci jeden krok wcześniej
        prev_arr_2d = None
        # stwórz sieć
        arr_2d = init_rand_arr_2d(L, p, K)
        
        # wyniki pojedynczej symulacji dla K i K/2 dla określonego prawdopodobieństwa
        sim_steps = []
        
        # liczba kroków czasowych dla pojedynczej symulacji
        t = 0
        
        # początkowe wartości dla K i K/2
        count_K, count_K_half = count_full_and_half_knowledge(arr_2d, K)
        # wykonuj wymulację dopóki wiedza aktorów nie będzie się zmieniała
        while True:      
            prev_arr_2d = np.copy(arr_2d)
            
            # którą cząstkę wiedzy wziąć od jednego z sąsiadów (dla każdego aktora)
            which_k = []

            # dla każdego aktora w sieci:
            for i in range(L):
                for j in range(L):
                    # zapisz sąsiadów..
                    curr_neighbors = [
                        arr_2d[i, (j - 1) % L], # lewo
                        arr_2d[i, (j + 1) % L],  # prawo
                        arr_2d[((i - 1) % L), j],   # góra
                        arr_2d[((i + 1) % L), j],   # dól
                    ]
                            
                    # wyjątki:
                    # dla pierwszego wiersza górny sąsiad jest z ostatniego wiersza
                    if i == 0:
                        curr_neighbors[2] = arr_2d[L - 1, j]
                    # dla ostatniego wiersza dolny sąsiad jest z pierwszego wiersza
                    if i == L - 1:
                        curr_neighbors[3] = arr_2d[0, j]
                    
                    # dla pierwszej kolumny lewy sąsiad jest z wcześniejszego wiersza, ostatniej kolumny
                    if j == 0:
                        curr_neighbors[0] = arr_2d[(i - 1) % L, L - 1]
                    # dla ostatniej kolumny prawy sąsiad jest z następnego wiersza, pierwszej kolumny
                    if j == L - 1:
                        curr_neighbors[1] = arr_2d[(i + 1) % L, 0]
                
                    # oblicz, ile czątek wiedzy mają poszczególni sąsiedzi
                    neighbors_k_count = [sum(1 for val in k if val == 1) for k in curr_neighbors]
                    # ile cząstek wiedzy ma obecny aktor
                    curr_k_count = arr_2d[i, j].count(1)
                    # którzy sąsiedzi mogą przekazać swoją cząstkę wiedzy (mają o jedną więcej)
                    better_neighbors = []
                    for idx, c in enumerate(neighbors_k_count):
                        if c == curr_k_count + 1:
                            better_neighbors.append([idx, curr_neighbors[idx]])
                            
                    # jeśli aktor ma sąsiada, który może go nauczyć
                    if better_neighbors:
                        # wylosuj jednego
                        chosen_neighbor = random.choice(better_neighbors)
                        idx, chosen = chosen_neighbor
                        mismatched_k = []
                        # sprawdź, których cząstek wiedzy nie ma obecny aktor w porównaniu do nauczyciela
                        for index, (val_curr, val_chosen) in enumerate(zip(arr_2d[i, j], chosen)):
                            if val_curr == 0 and val_chosen == 1:
                                mismatched_k.append(index)
                        # wybierz dowolną dostępną cząstkę wiedzy dla aktualnego aktora
                        if mismatched_k:
                            chosen_k = random.choice(mismatched_k)
                            which_k.append(chosen_k)
                    else:
                        # jeśli aktor nie ma sąsiada-nauczyciela
                        chosen_neighbor = None
                        which_k.append(None)

            # którą cząstkę wiedzy (na którym ineksie) ma się nauczyć każdy aktor
            which_k_idx = 0
            for i in range(L):
                for j in range(L):
                    if which_k[which_k_idx] is not None:
                        k_idx = which_k[which_k_idx]
                        arr_2d[i, j][k_idx] = 1
                        which_k_idx += 1
                    else:
                        which_k_idx += 1
            
            # wcześnijsze wartości K i K/2
            prev_count_K, prev_count_K_half = count_K, count_K_half
                
            # oblicz aktualne K i K/2
            count_K, count_K_half = count_full_and_half_knowledge(arr_2d, K)
            # zapamiętaj K i K/2 z aktualnego kroku aktualnej symulacji
            sim_steps.append((count_K, count_K_half))
            
            f.write(f'Liczba K = {count_K}, K/2 = {count_K_half}\n')
            
            t += 1
            
            # jeśli nastąpiła wcześniejsza iteracja symulacji
            if prev_arr_2d is not None:
                list1 = arr_2d.tolist()
                list2 = prev_arr_2d.tolist()
                # porównaj, czy sieć wcześniejsza i późniejsza są takie same i czy wystąpiły zmiany w K i K/2
                if list1 == list2 and prev_count_K == count_K and prev_count_K_half == count_K_half:
                    break
            
        # zapamiętaj rezultaty pojedynczej zakończonej symulacji
        simulations.append(sim_steps)
        f.write(f't = {t}\n\n')
        
    # zapamiętej rezultaty z wszystkich 50 symulacji dla określonego prawdopodobieństwa
    results.append(simulations)
    f.write('\n')


# rysuj wykres
plt.figure(figsize=(10, 6))

# dla każdego prawdopodobieństwa:
for idx, p in enumerate(probabs):
    # ile było maksymalnie kroków patrząc na każdą symulację
    max_steps = max(len(sim) for sim in results[idx])
    # inicjalizuj array'e z zerami maksymalnej długości symulacji
    # array'e mają przechowywać średnie wartości w każdym kroku czasowym
    avg_K = np.zeros(max_steps)
    avg_K_half = np.zeros(max_steps)
    
    # dla każdej symulacji w aktualnym prawdopodobieństwie:
    for sim in results[idx]:
        # konwertuj na array i oblicz, ile kroków czasowych miała symulacja
        sim = np.array(sim)
        sim_length = len(sim)
        # jeśli symulacja skończyła się wcześniej, wyrównaj do maksymalnej wartości dodając ostatnią wartość z symulacji
        if sim_length < max_steps:
            last_value = sim[-1]
            sim = np.vstack([sim, np.tile(last_value, (max_steps - sim_length, 1))])
        # dodaj liczbę aktorów z K i K/2 dla każdego kroku czasowego
        avg_K += sim[:, 0]
        avg_K_half += sim[:, 1]
    
    # oblicz średnią liczbę aktorów w każdym kroku czasowym, uśredniając po liczbie symulacji
    avg_K /= R
    avg_K_half /= R
    
    plt.plot(avg_K, label=f'Średnia $\\it{{n(K)}}$ dla $\\it{{p}}$={p}')
    plt.plot(avg_K_half, label=f'Średnia $\\it{{n(K/2)}}$ dla $\\it{{p}}$={p}')

plt.xlabel('$\\it{{t}}$')
plt.ylabel('Liczba aktorów $\\it{{n}}$')
plt.title('Dynamika transferu wiedzy')
plt.legend()
plt.grid(True)
plt.savefig('wykres.png')
plt.show()


f.close()
