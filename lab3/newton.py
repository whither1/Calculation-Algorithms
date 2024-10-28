EPS = 1e-8

def devided_dif(x0, y0, x1, y1):
    if abs(x0 - x1) > EPS:
        return (y0 - y1) / (x0 - x1)
    return 0

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
            table[index + j][1] = devided_dif(
                table[index + j][0],     table[index + j][1],
                table[index + j + i + 1][0], table[index + j + 1][1]
            )

        mul = 1

        for j in range(i + 1):
            mul *= x - table[index + j][0]

        mul *= table[index][1]

        res += mul
    
    return res