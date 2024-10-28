def get_bordered_table(array, x, deg):
    amount = deg + 1
    if len(array) < amount:
        return None
    if len(array) == amount:
        return array
    middle = -1
    left = amount // 2
    right = len(array) - left - 1
    for i in range(left, right + 1):
        if array[i].x > x:
            middle = i
            break
    if middle == -1:
        middle = right + 1
    return array[middle - left: middle + (amount - left)]


# Таблица разделённых разностей для полинома Ньютона
def get_diff_table(nodes):
    split_diffs = []
    arg_arr = [elem.x for elem in nodes]
    split_diffs.append([elem.y for elem in nodes])
    for i in range(len(nodes) - 1):
        diffs = []
        for j in range(len(nodes) - i - 1):
            new_diff = split_diffs[i][j + 1] - split_diffs[i][j]
            new_diff /= (arg_arr[j + i + 1] - arg_arr[j])
            diffs.append(new_diff)
        split_diffs.append(diffs)
    return split_diffs

# Функция считает полином Ньютона
def newton_calc(diff_table, nodes, x):
    arg_arr = [elem.x for elem in nodes]
    koefs = [elem[0] for elem in diff_table]
    answer = 0
    answer += koefs[0]
    for i in range(1, len(koefs)):
        elem = koefs[i]
        for j in range(i):
            elem *= (x - arg_arr[j])
        answer += elem
    return answer

def newton_calc_two_pol(diff_table, nodes, x):
    arg_arr = [elem.x for elem in nodes]
    koefs = [elem[0] for elem in diff_table]
    answer = 0
    answer += koefs[0]
    return 6 * x * koefs[3] + 2 * koefs[2] - 2 * koefs[3] * (arg_arr[0] + arg_arr[1] * arg_arr[2])
