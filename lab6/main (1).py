import numpy as np
import sympy as sp
import matplotlib.pyplot as plt


def t(k):
    return 1 / (k + 1)


def f(x, n):
    return (x * x - 1) ** n


def P(x, n):
    xs, ns = sp.symbols("xs ns")
    return (1 / ((2 ** n) * sp.factorial(n))) * sp.diff(f(xs, ns), xs, n).evalf(subs={xs: x, ns: n})


def diff_P(x, n):
    return (n / (1 - x * x)) * (P(x, n - 1) - x * P(x, n))


def find_roots(n):
    x = []
    k = 1000
    eps = 1e-8
    for i in range(1, n + 1):
        x.append(np.cos((np.pi * (4 * i - 1)) / (4 * n + 2)))
    for _ in range(k):
        xd = []
        for i in range(n):
            xd.append(-P(x[i], n) / diff_P(x[i], n))
            x[i] += xd[i]
        s = 0
        for elem in xd:
            s += elem * elem
        s **= 0.5
        if s < eps:
            return x
    return None


def simpson(x, f):
    xs = sp.symbols("x")
    n = 100
    h = x / n
    res = 0
    for i in range(n // 2 - 1):
        res += f(subs={xs: h * 2 * i}) + 4 * f(subs={xs: h * (2 * i + 1)}) + f(subs={xs: h * (2 * i + 2)})
    res *= h / 3
    return res


def func(x, y, xn, yn, zn):
    tmp = []
    for i in range(len(yn)):
        data = []
        for j in range(len(xn)):
            data.append((xn[j], zn[i][j]))
        tmp.append(sp.interpolate(data, x))

    data = []
    for i in range(len(yn)):
        data.append((yn[i], tmp[i]))

    return sp.interpolate(data, y)


def task_1(n, xn, yn, zn):
    xs = sp.symbols("x")
    pr = find_roots(n)
    mtx = []
    for i in range(len(pr)):
        mtx.append([])
        for j in range(len(pr)):
            mtx[i].append(float(pr[j] ** i))
    f = []
    for i in range(len(pr)):
        f.append(float(t(i)))
    solution = np.linalg.solve(mtx, f)
    res = 0
    for i in range(n):
        res += solution[i] * func(xs, pr[i], xn, yn, zn)

    return simpson(1, res.evalf)


def one_sided_diff(y0, y1, h):
    return (y1 - y0) / h


def central_diff(y0, y2, h):
    return (y2 - y0) / (2 * h)


def second_diff(y0, y1, y2, h):
    return (y0 - 2 * y1 + y2) / (h * h)


def runge(y0, y1, y2, h, m):
    return one_sided_diff(y0, y1, h) + (one_sided_diff(y0, y1, h) - one_sided_diff(y0, y2, m * h)) / (m - 1)


if __name__ == "__main__":
    print("Задание 1")
    n = 13
    xn = []
    yn = []
    zn = []
    with open("src.txt", "r") as file:
        xn = list(map(float, file.readline().split()[1:]))
        file.readline()
        while line := file.readline():
            line = line.split()
            yn.append(float(line[0]))
            zn.append(list(map(float, line[1:])))

    print(task_1(n, xn, yn, zn))
    print("Задание 2")
    print("x   y     1    2    3    4    5")

    x = list(range(1, 7))
    y = [0.571, 0.889, 1.091, 1.231, 1.333, 1.412]
    eta = list(map(lambda x: 1 / x, y))
    eps = list(map(lambda x: 1 / x, x))
    h = 1
    print(f"{x[0]} {y[0]} {round(one_sided_diff(y[0], y[1], h), 2):.2f} "
          f"{round((-3 * y[0] + 4 * y[1] - y[2]) / (2 * h), 2):.2f} "
          f"{round(runge(y[0], y[1], y[2], h, 2), 2):.2f} "
          f"{round((eta[1] - eta[0]) / (eps[1] - eps[0]) * (y[0] / x[0]), 2):.2f} "
          f"????")
    for i in range(1, 4):
        print(f"{x[i]} {y[i]} {round(one_sided_diff(y[i], y[i + 1], h), 2):.2f} "
              f"{round(central_diff(y[i - 1], y[i + 1], h), 2):.2f} "
              f"{round(runge(y[i], y[i + 1], y[i + 2], h, 2), 2):.2f} "
              f"{round((eta[i + 1] - eta[i]) / (eps[i + 1] - eps[i]) * (y[i] / x[i]), 2):.2f} "
              f"{round(second_diff(y[i - 1], y[i], y[i + 1], h), 2):.2f}")
    print(f"{x[i]} {y[i]} {round(one_sided_diff(y[i], y[i + 1], h), 2):.2f} "
              f"{round(central_diff(y[i - 1], y[i + 1], h), 2):.2f} "
              f"???? "
              f"{round((eta[i + 1] - eta[i]) / (eps[i + 1] - eps[i]) * (y[i] / x[i]), 2):.2f} "
              f"{round(second_diff(y[i - 1], y[i], y[i + 1], h), 2):.2f}")
    print(f"{x[5]} {y[5]} ???? "
          f"{round((3 * y[5] - 4 * y[4] + y[3]) / (2 * h), 2):.2f} "
          f"???? "
          f"???? "
          f"????")
