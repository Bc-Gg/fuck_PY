def main(func, error, a, b):
    fa = func(a)
    fb = func(b)
    while a <= b:
        x0 = (a + b) / 2
        fx0 = func(x0)
        if abs(fx0) < error:
            return x0
        if fa * fx0 < 0:
            b = x0
            fb = fx0
        elif fb * fx0 < 0:
            a = x0
            fa = fx0

if __name__ == '__main__':
    le, ri = -1, 2
    func = lambda x: x ** 2 - 4 * x + 3
    error = 10 ** -6
    solution = main(func, error, le, ri)
    print(f'在区间[{le}, {ri}]内，在{float(error)}的误差之下，方程的根为{solution}')


