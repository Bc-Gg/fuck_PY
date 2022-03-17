import re

def func(mystr,pattern) ->list:
    ret = []
    next_str = re.search(pattern,mystr,re.U)
    ss = next_str.group()
    while True:
        ret.append(ss)
        mystr = mystr[next_str.span()[1]:]
        if re.search(pattern, mystr, re.U) == None:
            break
        ss = re.search(pattern, mystr, re.U).group()
    return ret


def main():
    str = input()
    pattern = r'(([\u4e00-\u9fa5])*(\s)*)([\u4e00-\u9fa5])(:|：)((\d{3}-\d{8}|\d{4}-\d{7}|\d{7})(\s*)(,|，))*(\d{3}-\d{8}|\d{4}-\d{7}|\d{7})'
    number_list = func(str,pattern)
    for number in number_list:
        print(number)


if __name__ == '__main__':
    main()