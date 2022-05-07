import numpy as np

def init_lu(param):
    lens = len(param)
    # 必须加上dtype ，否则小数矩阵会报错
    l = np.zeros((lens,lens),dtype=float)
    u = np.zeros((lens,lens),dtype=float)
    for i in range(lens):
        l[i][i] = 1
        u[0][i] = param[0][i]
        l[i][0] = param[i][0] / u[0][0]
    for i in range(1,lens):
        u[i,i:] = param[i, i:] - np.sum(l[i, :i].reshape(i, 1) * u[:i, i:], axis=0)
        if i == lens-1 :
            continue
        l[i+1:,i] = (param[i + 1:, i] - np.sum(l[i + 1:, :i] * u[:i, i].reshape(1, i), axis=0)) / u[i][i]
    return l,u

def solve(l, u, val):
    l = np.hstack([l, val])
    m,n = l.shape
    for i in range(n-1):
        l[i + 1:, :] = l[i + 1:, :] - l[i] * l[i + 1:, i].reshape(m - i - 1, 1)
    val = l[:, -1].reshape(m, 1)
    u = np.hstack([u, val])
    for i in range(m-1):
        i = m-i-1
        u[:i, :] = u[:i, :] - u[i] * u[:i, i].reshape(i, 1) / u[i][i]

    for i in range(m):
        u[i][-1] = u[i][-1] / u[i][i]
        u[i][i] = 1
    return u[:, -1].reshape(m, 1)

def main():
    param = np.array([[4,-2,-4], [-2,17,10], [-4,10,9]])
    val = np.array([[-2],[25],[15]])
    print(param)
    print(val)
    l, u = init_lu(param)
    solution = solve(l, u, val)
    print(solution)



if __name__ == '__main__':
    main()