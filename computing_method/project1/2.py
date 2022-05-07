from sympy import *
x = symbols('x')
x0 = 3
x_list = [x0]
i = 0
# func
f = lambda x : x ** 2 - 2 * 4

while True:
    # 判断分母是否为0，如果是0直接跳出
    if diff(f(x),x).subs(x,x0) != 0:
        x0 = x0 - f(x0) / diff(f(x), x).subs(x, x0)
        x_list.append(x0)
    else:
        break
    if len(x_list) > 1:
        i += 1
        error = abs((x_list[-1] - x_list[-2]) / x_list[-1])
        if error < 10 ** (-6):
            print(f'迭代第{i}次后，误差小于10^(-6)，误差为{error}')
            break

print(f'所求方程式的根为{float(x_list[-1])}')
