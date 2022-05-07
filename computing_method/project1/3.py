import numpy as np


def get_index_of_maxval(param, ind):
    max_val = abs(param[ind][ind])
    max_ind = ind
    for i in range(ind, param.shape[0]):
        if abs(param[i][ind]) > max_val:
            max_val = abs(param[i][ind])
            max_ind = i
    return max_ind

def xchg_two_col(param ,a , b):
    temp = param[a]
    param[a] = param[b]
    param[b] = temp


def guess_method(param: np.array ,val :np.array):
    try:
        assert param.shape[0] == val.shape[0]
        for col in range(0,param.shape[0]):
            max_ind = get_index_of_maxval(param, col)
            xchg_two_col(param, max_ind, col)
            xchg_two_col(val , max_ind, col)
            for j in range(col + 1, param.shape[0]):
                if param[col][col] != 0:
                    main_factor = -(param[j][col] / param[col][col])
                else:
                    raise ValueError
                for k in range(col , param.shape[1]):
                    param[j][k] += main_factor * param[col][k]
                val[j][0] += main_factor * val[col]

    except AssertionError as e:
        print(e,"Assertion Error: param mat must have the same col with val mat")
    except ValueError as e:
        print(e,"this mat is singular matrix")
        exit()

def solve(param ,val):
    mat = np.zeros((param.shape[0], 1))
    if param[-1][-1] == 0:
        print("oh !this param mat is singular matrix")
        exit()
    else :
        mat[-1] = val[-1] / param[-1][-1]

    for i in range(param.shape[0]-2 , -1 ,-1):
        sum = 0
        for j in range(i+1, param.shape[0]):
            sum += param[i][j] * mat[j]
        mat[i] = (val[i] - sum) / param[i][i]
    return mat

def main():
    param = np.array([[4,-2,-4], [-2,17,10], [-4,10,9]])
    val = np.array([[-2],[25],[15]])
    print(param)
    print(val)
    guess_method(param,val)
    solution = solve(param,val)
    print(solution)


if __name__ == '__main__':
    main()