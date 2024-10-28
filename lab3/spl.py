import math as m
EPS = 10e-8

def calc_A(y_arr):
    return y_arr[:-1]

def calc_C(x_arr, y_arr):
    size = len(x_arr)

    C = [0] * (size - 1)

    ksi_arr = [0]
    teta_arr = [0]

    for i in range(2, size):
        h1 = x_arr[i] - x_arr[i - 1]
        h2 = x_arr[i - 1] - x_arr[i - 2]
        b = - 2 * (h2 + h1)
        a = h2
        d = h1

        fi = - 3 * ((y_arr[i] - y_arr[i - 1]) / d - (y_arr[i - 1] - y_arr[i - 2]) / a)
        #находим подгоночные коэффициенты
        ksi_cur = - d / (h2 * ksi_arr[i - 2] - b)
        teta_cur = (fi + a * teta_arr[i - 2]) / (b - a * ksi_arr[i - 2])

        ksi_arr.append(ksi_cur)
        teta_arr.append(teta_cur)

    for i in range(size - 3, 0, -1):
        C[i] = ksi_arr[i] * C[i + 1] + teta_arr[i]

    return C

def calc_B_and_D(x_arr, y_arr, C):
    B = []
    D = []

    size = len(x_arr)

    for i in range(1, size - 1):
        h = x_arr[i] - x_arr[i - 1]

        B.append((y_arr[i] - y_arr[i - 1]) / h - (h * (C[i] + 2 * C[i - 1])) / 3)
        D.append((C[i] - C[i - 1]) / (3 * h))

    h = x_arr[-1] - x_arr[-2]

    B.append((y_arr[-1] - y_arr[-2]) / h - (h * 2 * C[-1]) / 3)
    D.append(-C[-1] / (3 * h))

    return B, D

def calculate_koefs_spline(x_arr, y_arr):
    A = calc_A(y_arr)
    C = calc_C(x_arr, y_arr)
    B, D = calc_B_and_D(x_arr, y_arr, C)

    return A, B, C, D

def fined_index(x_arr, x):
    size = len(x_arr)
    index = 1

    while (index < size and x_arr[index] < x):
        index += 1

    return index - 1

def count_polynom(x, x_arr, index, koefs):
    h = x - x_arr[index]
    y = 0

    for i in range(4):
        y += koefs[i][index] * (h ** i)

    return y

def spline(table, x):
    x_arr = [i[0] for i in table]
    y_arr = [i[1] for i in table]

    coefs = calculate_koefs_spline(x_arr, y_arr)

    index = fined_index(x_arr, x)

    y = count_polynom(x, x_arr, index, coefs)

    return y

def create_data_from_draw(x_arr, y_arr, m):
    x_interval = []
    y_interval = []
    x = 0
    x_next = x_arr[1]
    x_prev = 0
    i = 0
    a, b, c, d = calculate_koefs_spline(x_arr, y_arr, m)
    while x < 7:
        x_interval.append(x)
        if x > x_next:
            i += 1
            x_prev = x_next
            x_next = x_arr[i + 1]
        y_interval.append(a[i] + b[i]*(x - x_prev) + c[i]*(x - x_prev)**2 + d[i]*(x - x_prev)**3)
        x += 0.01
    return x_interval, y_interval
