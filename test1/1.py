import re

def find_func(str):
    pa = r'([\u4e00-\u9fa5]*)(\u53a6\u95e8)([\u4e00-\u9fa5]*)(\s|)([0-9]*)([\u4e00-\u9fa5]*)'
    org = re.search(pa,str,re.U)
    if org:
        return org.group()
    return None

def func(mystr,pattern) ->list:
    ret = []
    next_str = re.search(pattern,mystr,re.U)
    ss = next_str.group()
    while True:
        ret.append(ss)
        mystr = mystr[next_str.span()[1]:]
        # print(f'mystr:{mystr}')
        if re.search(pattern, mystr, re.U) == None:
            break
        next_str = re.search(pattern, mystr, re.U)
        ss = next_str.group()
    return ret

def main():
    str = input()
    sstr = str
    pattern = r'(([\u4e00-\u9fa5]|[a-zA-z])*(\s)*)([\u4e00-\u9fa5]|[a-zA-z])(:|：)((((\d{11})|((\d{7,8})|(\d{4}|\d{3})-(\d{7,8})|(\d{4}|\d{3})-(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1})|(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1})))(\s*)(,|，))*)((\d{11})|((\d{7,8})|(\d{4}|\d{3})-(\d{7,8})|(\d{4}|\d{3})-(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1})|(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1})))'
    org = find_func(sstr)
    number_list = func(str,pattern)
    print(org)
    # print(number_list)
    for number in number_list:
        print(number)


if __name__ == '__main__':
    main()