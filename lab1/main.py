from copy import deepcopy
EPS = 1e-8

def read_file(filename):
    try:
        with open(filename, 'r') as file:
            table = [[float(num) for num in string.split()] for string in file.readlines()]
        return table
    except:
        return []
    
def input_params(len):
    running = True
    while running:
        try:
            n = int(input("Введите степень полинома: "))
        except:
            print("Необходимо ввести целое число")
            continue
        if (n >= len):
            print("Слишком большая степень аппроксимирующего полинома для данной таблицы")
            continue
        elif (n <= 0):
            print("Степень должна быть больше 0")
            continue
        running = False
    running = True
    while running:
        try:
            x = float(input("Введите значение аргумента: "))
        except:
            print("Необходимо ввести вещественное число")
            continue
        running = False
    return n, x

def print_table(table):
    print("\n{:^12}{:^12}{:^12}{:^12}{:^12}{:^12}\n".format("x\y при n", "1", "2", "3", "4", '5'))

    for i in range(len(table)):
        for j in range(len(table[i])):
            print("%-12.3f" %(table[i][j]), end = '')
        print()

    print()

def devided_dif(x0, y0, x1, y1, y_def):
    if abs(x0 - x1) > EPS:
        return 0, (y0 - y1) / (x0 - x1)
    return 1, y_def

def get_index_newton(table, n, x):
    index = 0

    for row in table:
        if row[0] > x:
            break
        index += 1
    
    if index >= len(table) - n:
        return len(table) - n - 1
    
    l_range = r_range = index

    for _ in range(n):
        if r_range - index == index - l_range:
            if l_range:
                l_range -= 1
            elif not l_range:
                break
            else:
                r_range += 1
        else:
            if r_range < len(table) - 1:
                r_range += 1
            else:
                l_range -= 1
    
    return l_range

def get_index_ermit(table, n, x):
    index = 0

    for row in table:
        if row[0] > x:
            break
        index += 1
    
    if index >= len(table) - n:
        return len(table) - (n + (3 - n % 3))

    return index - 3
    
def newton_polynom(table, n, x):
    index = get_index_newton(table, n, x)

    res = table[index][1]

    for i in range(n):
        for j in range(n - i):
            flag, table[index + j][1] = devided_dif(
                table[index + j][0],     table[index + j][1],
                table[index + j + i + 1][0], table[index + j + 1][1],
                table[index + j][2]
            )

        mul = 1

        for j in range(i + 1):
            mul *= x - table[index + j][0]

        mul *= table[index][1]

        res += mul
    
    return res

def ermit_polynom(table, n, x):
    new_size = len(table) * 3
    for i in range(0, new_size, 3):
        table.insert(i + 1, table[i][:])
        table.insert(i + 2, table[i][:])
    
    index = get_index_ermit(table, n, x)

    res = table[index][1]

    for i in range(n):
        for j in range(n - i):
            flag, table[index + j][1] = devided_dif(
                table[index + j][0],     table[index + j][1],
                table[index + j + i + 1][0], table[index + j + 1][1],
                table[index + j][2]
            )
            if flag:
                table[index + j][2] = table[index + j][3]

        mul = 1

        for j in range(i + 1):
            mul *= x - table[index + j][0]

        mul *= table[index][1]

        res += mul
    
    return res

def find_root_newton(table, n):
    for row in table:
        row[0], row[1] = row[1], row[0]

    # table.sort(key = lambda array: array[0])

    return newton_polynom(table, n, 0)    

def find_root_ermit(table, n):
    for row in table:
        row[0], row[1] = row[1], row[0]
        row[3] = -row[3] / row[2] ** 3
        row[2] = 1 / row[2]
    
    # table.sort(key = lambda array: array[0])
    
    return ermit_polynom(table, n, 0)

def task_1(table):
    step = 0.1

    answer_newton = []
    x = table[0][0]
    while x < table[-1][0] + step:
        answer_newton.append([x] + [newton_polynom(deepcopy(table), i, x) for i in range(1, 6)])
        x += step
    
    answer_ermit = []
    x = table[0][0]
    while x < table[-1][0] + step:
        answer_ermit.append([x] + [ermit_polynom(deepcopy(table), i, x) for i in range(1, 6)])
        x += step
    
    return answer_newton, answer_ermit

def task_3():
    filename1 = 'task3_1'
    filename2 = 'task3_2'

    table1 = read_file(filename1)
    table2 = read_file(filename2)

    for row in table1:
        row[0], row[1] = row[1], row[0]
    
    new_table1 = []

    for row in table2:
        new_table1.append([row[0], newton_polynom(deepcopy(table1), 3, row[0]) - row[1], row[2]])

    for row in new_table1:
        row[0], row[1] = row[1], row[0]

    new_table1.sort(key = lambda array: array[0])

    x = newton_polynom(new_table1, 3, 0)
    # y1 = newton_polynom(table1, 3, x)
    y2 = newton_polynom(table2, 3, x)
    return x, y2

def main():
    filename = "data"
    table = read_file(filename)
    if not table:
        return -11
    n, x = input_params(len(table))
    # x = float(input("Сюда: "))

    y1 = newton_polynom(deepcopy(table), n, x)
    y2 = ermit_polynom(deepcopy(table), n, x)

    print(f"Значение функции полиномом Ньютона: {y1}\nЗначение функции полиномом Эрмита: {y2}")
    answer_newton, answer_ermit = task_1(deepcopy(table))

    print("Таблица значений y(x) при n = 1 - 5 для полинома Ньютона")
    print_table(answer_newton)
    
    print("Таблица значений y(x) при n = 1 - 5 для полинома Эрмита")
    print_table(answer_ermit)
    
    # n += 1
    # ep = ermit_polynom(deepcopy(table), n, x)
    # np = 0
    np = find_root_newton(deepcopy(table), n)
    # table = read_file(filename)
    # if not table:
        # return -11
    ep = find_root_ermit(deepcopy(table), n)

    print(f'{np} - Корень, вычисленный полиномом Ньютона\n{ep} - Корень, вычисленный полиномом Эрмита')

    ans = task_3()

    print(f'Решение системы уравнений: {ans}')


if __name__ == '__main__':
    main()