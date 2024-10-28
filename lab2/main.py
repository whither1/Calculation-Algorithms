from spl import create_data_from_draw
from newton import get_bordered_table, get_diff_table, newton_calc, newton_calc_two_pol
import matplotlib.pyplot as plt
from point_struct import Point
def read_file(name_file):
    try:
        with open(name_file, "r") as f:
            table = [list(map(float, string.split())) for string in list(f)]
        return table

    except:
        print("Ошибка чтения файла!\n")
        return []

def read_table(filename):
    table = []
    file = open(filename)

    for line in file.readlines():
        row = list(map(float, line.split(" ")))
        table.append(Point(row[0], row[1]))

    file.close()
    return table

def print_table(table):
    print("\n{:^5}{:^11}\n".format("x", "y"))

    for i in range(len(table)):
        for j in range(len(table[i])):
            print("%-8.3f" %(table[i][j]), end = '')
        print()

    print()

def read_data():
    try:
        rc = int(input("Выберете способ задания условий:\n"
                       "1 - Естественные краевые условия\n"
                       "2 - На одной границе вторая производная сплайна равна третьей производной Ньютона\n"
                       "3 - На двух границах вторая производная сплайна равна третьей производной Ньютона\n"))
        if (rc > 3) or (rc < 1):
            print("Ошибка ввода\n")
            return 1
        return rc
    except:
        print("Ошибка ввода\n")
        return 1

def main():
    name_file = "data/test1.txt"

    table = read_file(name_file)
    init_table = read_table(name_file)
    if (table == []):
        return

    table.sort(key = lambda array: array[0])
    print_table(table)
    x_arr = []
    y_arr = []
    for i in range(len(table)):
        x_arr.append(table[i][0])
        y_arr.append(table[i][1])

    rc = read_data()
    m = [0, 0]
    if rc == 1:
        m = [0, 0]
    if rc == 2:
        table_1 = get_bordered_table(init_table, x_arr[0], 3)
        diff_table = get_diff_table(table_1)
        newton_polynom = newton_calc_two_pol(diff_table, table_1, x_arr[0])
        m = [newton_polynom, 0]
    if rc == 3:
        table_1 = get_bordered_table(init_table, x_arr[0], 3)
        diff_table = get_diff_table(table_1)
        newton_polynom_1 = newton_calc_two_pol(diff_table, table_1, x_arr[0])
        table_1 = get_bordered_table(init_table, x_arr[-1], 3)
        diff_table = get_diff_table(table_1)
        newton_polynom_2 = newton_calc_two_pol(diff_table, table_1, x_arr[-1])
        m = [newton_polynom_1, newton_polynom_2]

    x, y = create_data_from_draw(x_arr, y_arr, m)
    plt.plot(x, y)
    yi = []
    for xi in x:
        table_1 = get_bordered_table(init_table, xi, 3)
        diff_table = get_diff_table(table_1)
        newton_polynom = newton_calc(diff_table, table_1, xi)
        yi.append(newton_polynom)
    plt.plot(x, yi)
    plt.show()

if __name__ == "__main__":
    main()