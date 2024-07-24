import numpy as np


def init_arr_2d():
  '''
  Funkcja inicjalizuje macierz 2D z losowo rozmieszczonymi 0 i 1
  Zwraca macierz 2D.
  '''
  arr_1d = np.array([1] * HALF_ELEMS + [-1] * HALF_ELEMS)
  # przemieszaj wartości 1 i -1
  np.random.shuffle(arr_1d)
  # zrób z tego macierz 2D 10x10
  arr_2d = arr_1d.reshape((ROWS, COLS))

  return arr_2d


def print_and_write_arr(arr_2d, ones_count):
  '''
  Funkcja wypisuje w konsoli sieć i jej gęstość.
  arr_2d: słownik 2D
  ones_count: aktualna liczba 1 w sieci
  '''
  print(f'Gęstość początkowa 1: {ones_count}')
  f.write(f'Gęstość początkowa 1: {ones_count}\n')
  print(arr_2d, end='\n\n')
  f.write(str(arr_2d) + '\n\n')


def draw_info(el1, rand_row_idx, rand_col_idx, direction):
  '''
  Funkcja wypisuje informacje o wylosowanej parze uzgodnionych elementów.
  el1: wylosowany pierwszy element uzgodnionej pary
  rand_row_idx: wylosowany indeks wiersza
  rand_col_idx: wylosowany indeks kolumny
  '''
  print(f'Wartość uzgodnionej pary: {el1}')
  f.write(f'Wartość uzgodnionej pary: {el1}\n')
  print('Współrzędne wylosowanych elementów:', end=' ')
  f.write('Współrzędne wylosowanych elementów:\n')
  print(f'el1: ({rand_row_idx}, {rand_col_idx})')
  f.write(f'el1: ({rand_row_idx}, {rand_col_idx}), ')

  if direction == 0:
      print(f'el2: ({rand_row_idx}, {(rand_col_idx + nb_idx) % COLS})')
      f.write(f'el2: ({rand_row_idx}, {(rand_col_idx + nb_idx) % COLS})\n')
  else:
    print(f'el2: ({(rand_row_idx + nb_idx) % ROWS}, {rand_col_idx})')
    f.write(f'el2: ({(rand_row_idx + nb_idx) % ROWS}, {rand_col_idx})\n')


# inicjalizacja wymiarów macierzy
ROWS = 10
COLS = 10
ARR_DIM = ROWS * COLS

HALF_ELEMS = ARR_DIM // 2

f = open('zad1_wynik.txt', 'w')

# zwiekszaj t (czas wykonywania symulacji) co iterację
t = 0

# stwórz macierz 50:50 o wartościach 1 i -1
arr_2d = init_arr_2d()

ones_count = np.count_nonzero(arr_2d == 1)

# wypisz stan początkowy sieci
print_and_write_arr(arr_2d, ones_count)

# wykonuj do czasu, kiedy dojdziesz do 10 szczęśliwych trafów
att = 0
while att < 10:
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

  # sprawdź, czy wylosowana para ma te same wartości (para jest uzgodniona)
  # zgoda pary - zmiana sąsiadów, niezgoda - bez zmian
  if el1 == el2:
    # jeśli tak, to uzgodnij sasiadow
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

    # szczęśliwy traf ("na tak")
    att += 1

    ones_count = np.count_nonzero(arr_2d == 1)

    draw_info(el1, rand_row_idx, rand_col_idx, direction)
    print_and_write_arr(arr_2d, ones_count)
  else:
    # "spalony" traf zeruje obliczanie
    att = 0
  # zwiększ czas (numer przejścia sprawdzania) symulacji
  t += 1

print('-----')
f.write('-----\n')
print(f'Czas symulacji: {t} iteracji')
f.write(f'Czas symulacji: {t} iteracji\n')

f.close()