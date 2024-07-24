import numpy as np
import matplotlib.pyplot as plt


def init_arr_2d():
  '''
  Funkcja inicjalizuje macierz 2D z losowo rozmieszczonymi 0 i 1
  Zwraca macierz 2D.
  '''
  arr_1d = np.array([1] * int(ones_den) + [-1] * int(ARR_DIM - ones_den))
  # przemieszaj wartości
  np.random.shuffle(arr_1d)
  # zrób z tego macierz 2D NxN
  arr_2d = arr_1d.reshape((ROWS, COLS))

  return arr_2d


# inicjalizacja macierzy, zwiększ rozmiar układu
ROWS = 20
COLS = 20
# ROWS = 40
# COLS = 40
ARR_DIM = ROWS * COLS

f = open('zad3_wynik.txt', 'w')

# zwiekszaj t (czas wykonywania symulacji) co iterację
t = 0

# gęstości 1
ones_den_per = [0.25, 0.5, 0.75]
# liczba symulacji R do wykonania
sim_num = [10, 10**2, 10**3]
# sim_num = [10, 10**3, 10**5]

table_data = []

# przechodź po kolejnych R
for i in sim_num:
  # przechodź po kolejnych gęstościach
  for ones_den_per_it in ones_den_per:
    # poszczególne symulacje dla wybranego R
    # liczba 1 dla wszystkich symulacji wybranego R
    ones_count_sims = []
    for j in range(i):
      # lista do przechowywania liczby jedynek w kolejnych iteracjach
      ones_count_list = []
      # gęstość 1 w kolejnych iteracjach
      ones_den_list = []

      ones_count = -1
      ones_count_1st_it = -1

      ones_den = ARR_DIM * ones_den_per_it

      # stwórz macierz o wartościach 1 i -1
      arr_2d = init_arr_2d()

      # wykonuj do ustalonego limitu czasu
      # while t != 10000:
      while not (ones_count == arr_2d.size or ones_count == 0):
        # zapamiętaj początkową liczbę 1 i gęstość
        if t == 0:
          ones_count_1st_it = np.count_nonzero(arr_2d == 1)
          ones_count_list.append(ones_count_1st_it)
          ones_den_list.append(ones_count_1st_it / ARR_DIM * 100)


        # wylosuj 2 elementy, losowo pion lub poziom:
        # losuj współrzędne pierwszego elementu
        rand_row_idx = np.random.randint(0, ROWS)
        rand_col_idx = np.random.randint(0, COLS)
        el1 = arr_2d[rand_row_idx][rand_col_idx]

        # wylosuj, czy para w poziomie (0) czy w pionie (1)
        direction = np.random.randint(2)
        # dla wiersza losuj sąsiada lewo/prawo, dla kolumny losuj sąsiada góra/dół
        nb_idx = np.random.choice([-1, 1])
        if direction == 0:
          # przy wyborze wiersza losuj kolumnę
          el2 = arr_2d[rand_row_idx][(rand_col_idx + nb_idx) % COLS]
        else:
          # przy wyborze kolumny losuj wiersz
          el2 = arr_2d[(rand_row_idx + nb_idx) % ROWS][rand_col_idx]

        # sprawdz, czy wylosowana para ma te same wartosci (para jest uzgodniona)
        # zgoda pary - zmiana sąsiadów, niezgoda - bez zmian
        if el1 == el2:
          # jesli tak, to uzgodnij sasiadow
          if direction == 0:
            # sąsiad w tym samym rzędzie, po prawej stronie
            if nb_idx == 1:
              arr_2d[rand_row_idx][(rand_col_idx - 1) % COLS] = el1
              arr_2d[(rand_row_idx - 1) % ROWS][rand_col_idx] = el1
              arr_2d[(rand_row_idx + 1) % ROWS][rand_col_idx] = el1

              arr_2d[rand_row_idx][(rand_col_idx + 2) % COLS] = el1
              arr_2d[(rand_row_idx - 1) % ROWS][(rand_col_idx + 1) % COLS] = el1
              arr_2d[(rand_row_idx + 1) % ROWS][(rand_col_idx + 1) % COLS] = el1
            # sąsiad w tym samym rzędzie, po lewej stronie
            else:
              arr_2d[rand_row_idx][(rand_col_idx + 1) % COLS] = el1
              arr_2d[(rand_row_idx - 1) % ROWS][rand_col_idx] = el1
              arr_2d[(rand_row_idx + 1) % ROWS][rand_col_idx] = el1

              arr_2d[rand_row_idx][(rand_col_idx - 2) % COLS] = el1
              arr_2d[(rand_row_idx - 1) % ROWS][(rand_col_idx - 1) % COLS] = el1
              arr_2d[(rand_row_idx + 1) % ROWS][(rand_col_idx - 1) % COLS] = el1
          else:
            # sąsiad w tej samej kolumnie, poniżej
            if nb_idx == 1:
              arr_2d[(rand_row_idx - 1) % ROWS][rand_col_idx] = el1
              arr_2d[rand_row_idx][(rand_col_idx - 1) % COLS] = el1
              arr_2d[rand_row_idx][(rand_col_idx + 1) % COLS] = el1

              arr_2d[(rand_row_idx + 2) % ROWS][rand_col_idx] = el1
              arr_2d[(rand_row_idx + 1) % ROWS][(rand_col_idx - 1) % COLS] = el1
              arr_2d[(rand_row_idx + 1) % ROWS][(rand_col_idx + 1) % COLS] = el1
            # sąsiad w tej samej kolumnie, powyżej
            else:
              arr_2d[(rand_row_idx + 1) % ROWS][rand_col_idx] = el1
              arr_2d[rand_row_idx][(rand_col_idx - 1) % COLS] = el1
              arr_2d[rand_row_idx][(rand_col_idx + 1) % COLS] = el1

              arr_2d[(rand_row_idx - 2) % ROWS][rand_col_idx] = el1
              arr_2d[(rand_row_idx - 1) % ROWS][(rand_col_idx - 1) % COLS] = el1
              arr_2d[(rand_row_idx - 1) % ROWS][(rand_col_idx + 1) % COLS] = el1

        t += 1

        # liczba 1 w macierzy
        ones_count = np.count_nonzero(arr_2d == 1)
        ones_count_list.append(ones_count)

        ones_den_list.append(ones_count / ARR_DIM * 100)

      # print(
      #       f'Symulacja {j} dla R = {i}, p(%) = {ones_den_per_it}: t = {t}, p0 = {ones_count_1st_it}, p = {ones_count}'
      #   )

      # resetuj timer
      t = 0
      # dodaj wynik symulacji do listy wyników kolejnych symulacji
      ones_count_sims.append(ones_count)

    # średnia dla Rn
    sims_mean = sum(ones_count_sims) / i
    sim_mean_per = sims_mean / ARR_DIM * 100

    std_dev = np.std(ones_count_sims)
    mean_uncert = std_dev / np.sqrt(i)

    # mean_uncert_per = (mean_uncert / sims_mean) * 100
    print(f'Średnia z {i} symulacji dla p0 = {ones_den_per_it}: {sims_mean} ({sim_mean_per}%). Niepewność średniej: {mean_uncert}')
    f.write(f'Średnia z {i} symulacji dla p0 = {ones_den_per_it}: {sims_mean} ({sim_mean_per}%). Niepewność średniej: {mean_uncert}\n')

    table_data.append([i, ones_den_per_it, ones_count_1st_it, sims_mean, mean_uncert])

# wyświetlenie tabeli
headers = ['R', r'$\rho_0$ (%)', r'$\rho_0$', r'<$\rho_\infty$>', 'Niepewność średniej']
print("\t".join(headers))
for row in table_data:
    print("\t".join(map(str, row)))

# wizualizacja danych w tabeli
fig, ax = plt.subplots()
ax.axis('tight')
ax.axis('off')
ax.table(cellText=table_data, colLabels=headers, cellLoc='center', loc='center')

fig.set_size_inches(18, 10)
plt.savefig('tabela.png')
plt.show()

f.close()