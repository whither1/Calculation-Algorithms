from spl import spline
from newton import newton_polynom

Z_COUNT = 5

def read_file(filename):
    # try:
    with open(filename, 'r') as file:
        string = file.readline()
        i = 0
        table = []
        row = []
        while string:
            row.append(list(map(float, string.split())))
            i += 1
            if not (i % Z_COUNT):
                table.append(row)
                row = []
            string = file.readline()
    return table
    # except:
        # return []

def input_params():
    running = True
    while running:
        try:
            type = int(input('''Выберите способ интерполяции:
                             1 - Полином Ньютона
                             2 - Сплайн
                             3 - Смешанная интерполяция\n'''))
            if type < 1 or type > 3:
                raise Exception
        except:
            print("Необходимо ввести целое число от 1 до 3")
            continue
        running = False

    nx, ny, nz = 0, 0, 0
    running = True
    if type % 2:
        while running:
            try:
                nx, ny, nz = map(int, input("Введите степени полинома nx, ny, nz: ").strip().split())
            except:
                print("Необходимо ввести целое число")
                continue
            if nx <= 0 or ny <= 0 or nz <= 0:
                print("Степень должна быть больше 0")
                continue
            running = False

    running = True
    while running:
        try:
            x, y, z = map(float, input("Введите значения аргументов x, y, z: ").strip().split())
        except:
            print("Необходимо ввести вещественное число")
            continue
        running = False

    return type, (nx, ny, nz), (x, y, z)

def multivariate_interpolation_newton(table, nx, ny, nz, x, y, z):
    xn = list(range(5))
    yn = list(range(5))
    zn = list(range(5))
    zy_array = []

    for i in zn:
        y_array = []
        for j in yn:
            array = []
            for k in xn:
                array.append([k, table[i][j][k]])
            y_array.append(newton_polynom(array, nx, x))
        zy_array.append(y_array)

    z_array = []
    for i in zn:
        array = []
        for j in yn:
            array.append([j, zy_array[i][j]])
        z_array.append(newton_polynom(array, ny, y))
    
    array = []
    for i in zn:
        array.append([i, z_array[i]])

    return newton_polynom(array, nz, z)

def multivariate_interpolation_spline(table, x, y, z):
    xn = list(range(5))
    yn = list(range(5))
    zn = list(range(5))
    zy_array = []

    for i in zn:
        y_array = []
        for j in yn:
            array = []
            for k in xn:
                array.append([k, table[i][j][k]])
            y_array.append(spline(array, x))
        zy_array.append(y_array)

    z_array = []
    for i in zn:
        array = []
        for j in yn:
            array.append([j, zy_array[i][j]])
        z_array.append(spline(array, y))
    
    array = []
    for i in zn:
        array.append([i, z_array[i]])

    return spline(array, z)

def multivariate_interpolation_mixed(table, nx, ny, nz, x, y, z):
    xn = list(range(5))
    yn = list(range(5))
    zn = list(range(5))
    zy_array = []

    for i in zn:
        y_array = []
        for j in yn:
            array = []
            for k in xn:
                array.append([k, table[i][j][k]])
            y_array.append(newton_polynom(array, nx, x))
        zy_array.append(y_array)

    z_array = []
    for i in zn:
        array = []
        for j in yn:
            array.append([j, zy_array[i][j]])
        z_array.append(spline(array, y))
    
    array = []
    for i in zn:
        array.append([i, z_array[i]])

    return newton_polynom(array, nz, z)

def main():
    filename = "/home/whither/CalcAlgs/lab3/data"
    table = read_file(filename)
    if not table:
        return -11
    type, n, v = input_params()

    if type == 1:
        res = multivariate_interpolation_newton(table, *n, *v)
    
    elif type == 2:
        res = multivariate_interpolation_spline(table, *v)
    
    elif type == 3:
        res = multivariate_interpolation_mixed(table, *n, *v)

    print(f"Результат интерполяции выбранным методом: {res}")

if __name__ == '__main__':
    main()