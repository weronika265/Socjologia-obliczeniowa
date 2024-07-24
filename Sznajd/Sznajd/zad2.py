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


def sim_info(ones_den_per_it, ones_count_1st_it, ones_count, t):
  '''
  Funkcja wyświetla informacje o symulacji.
  ones_den_per_it: końcowa gęstość 1 dla symulacji
  ones_count_1st_it: liczba 1 w pierwszej iteracji symulacji
  ones_count: końcowa liczba 1 dla symulacji
  t: czas trwania symulacji
  '''
  print('-----')
  print(ones_den_per_it)
  print(f'W chwili początkowej liczba 1 = {ones_count_1st_it}')
  print(f'Końcowa liczba 1 = {ones_count}')
  print(f'Czas symulacji: {t} iteracji')


# inicjalizacja macierzy, zwiększ rozmiar układu
ROWS = 40
COLS = 40
ARR_DIM = ROWS * COLS

# zwiekszaj t (czas wykonywania symulacji) co iterację
t = 0

# gęstości 1
ones_den_per = [0.1, 0.25, 0.5, 0.75, 0.9]

# przechodź po kolejnych gęstościach
for ones_den_per_it in ones_den_per:
  # lista do przechowywania liczby jedynek w kolejnych iteracjach
  ones_count_list = []
  # gęstość 1 w kolejnych iteracjach
  ones_den_list = []

  ones_count = -1
  ones_count_1st_it = -1

  ones_den = ARR_DIM * ones_den_per_it

  # stwórz macierz o wartościach 1 i -1
  arr_2d = init_arr_2d()

  # wykonuj do czasu, kiedy dojdzie do pełnej zgody tak/nie
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
    # aktualna gęstość sieci
    ones_den_list.append(ones_count / ARR_DIM * 100)

  sim_info(ones_den_per_it, ones_count_1st_it, ones_count, t)

  # rysuj wykres
  plt.plot(range(len(ones_den_list)), ones_den_list, label=r'$\rho_0=$'f'{ones_den_per_it}')

  # resetuj timer
  t = 0

# dodaj etykiety do wykresu
plt.xlabel('t')
plt.ylabel(r'$\rho$ ' + '(%)')
plt.title(f'Czasowa ewolucja "na tak" dla {ARR_DIM} aktorów')
plt.legend()
plt.savefig('wykres_p(t).png')
plt.show()