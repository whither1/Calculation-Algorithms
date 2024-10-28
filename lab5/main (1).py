import numpy as np
import matplotlib.pyplot as plt
import math as m

n = 100
k = 1000
eps = 1e-8


def f1(x, y, z):
    return x ** 2 + y ** 2 + z ** 2 - 1


def f2(x, y, z):
    return 2 * x ** 2 + y ** 2 - 4 * z


def f3(x, y, z):
    return 3 * x ** 2 - 4 * y + z ** 2


def W_matrix(x):
    w = []
    w.append([2 * x[0], 2 * x[1], 2 * x[2]])
    w.append([4 * x[0], 2 * x[1], -4])
    w.append([6 * x[0], -4, 2 * x[2]])
    return w


def newton_method(xn):
    x_n = np.array(xn)
    for i in range(k):
        w = W_matrix(x_n)
        f = [-float(f1(x_n[0], x_n[1], x_n[2])),
             -float(f2(x_n[0], x_n[1], x_n[2])),
             -float(f3(x_n[0], x_n[1], x_n[2]))]
        sol = np.linalg.solve(w, f)
        x_n += sol
        s = 0
        for delta in sol:
            s += delta ** 2
        s = m.sqrt(s)
        if s < eps:
            return x_n

    return None

def laplace_func(x):
    return (2 / m.sqrt(2 * m.pi)) * m.exp(-x ** 2 / 2)

def tr(x, f):
    h = x / n
    area = 0
    x_tmp = 0
    for i in range(n):
        area += h * (f(x_tmp) + f(x_tmp + h)) / 2
        x_tmp += h
    return area

def laplace_check(x):
    sol = tr(x, laplace_func)
    if abs(sol) > 1:
        return np.sign(sol)
    return sol

def find_x(f):
    b = -15
    e = 15
    c = (e + b) / 2
    fc = laplace_check(c)
    while abs(f - fc) > eps:
        if f < fc:
            e = c
        else:
            b = c
        c = (e + b) / 2
        fc = laplace_check(c)
    return c

def free_f(y):
    h = 1 / n
    f = np.zeros(n + 1)
    f[0] = y[0] - 1
    f[n] = y[n] - 3

    for i in range(1, n):
        f[i] = -float((y[i - 1] - 2 * y[i] + y[i + 1]) / (h ** 2) - y[i] ** 3 - (i * h) ** 2)
    return f

def W_3(y):
    h = 1 / n
    w = np.zeros((n + 1, n + 1))
    w[0][0] = 1.0
    w[n][n] = 1.0

    for i in range(1, n):
        w[i][i - 1] = 1.0 / h ** 2
        w[i][i] = -2.0 / h ** 2 - 3.0 * y[i] ** 2
        w[i][i + 1] = 1.0 / h ** 2
    return w

def newton_method_3(y):
    x_n = np.array(y)
    for i in range(k):
        w = W_3(x_n)
        f = free_f(x_n)
        sol = np.linalg.solve(w, f)
        x_n += sol
        s = 0
        for delta in sol:
            s += delta ** 2
        s = m.sqrt(s)
        if s < eps:
            return x_n
    return None

def ex_3():
    h = 1 / n
    x = [i * h for i in range(n + 1)]
    y = [2 * x[i] + 1 for i in range(n + 1)]
    y_new = newton_method_3(y)
    return x, y_new

if __name__ == "__main__":
    print("Решение системы нелинейных уравнений")
    x0 = float(input("Введите начальное приближение x: "))
    y0 = float(input("Введите начальное приближение y: "))
    z0 = float(input("Введите начальное приближение z: "))

    res = newton_method([x0, y0, z0])

    print(f"Результат:\nx = {res[0]}\ny = {res[1]}\nz = {res[2]}")
    print("Поиск аргумента функции Лапласа по её значению")
    f = float(input("Введите значение функции Лапласа (от -1 до 1): "))
    print("Аргумент функции Лапласа равен: ", find_x(f))

    x, y = ex_3()
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.plot(x, y)
    plt.show()
