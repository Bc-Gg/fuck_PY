import struct
import psutil
import os
from binary_writer import *
def binary_reader():
    hash_table = []
    with open('hash_table.txt','rb') as fp:
        for _ in range(10000000):
            context = fp.read(3).hex()
            hash_table.append(eval('0x'+context))
    fp.close()
    return hash_table

def append_bin(hash_list):
    with open('hash_table.txt','ab') as fp:
        for hash_val in hash_list:
            # print((hash_val))
            temp_list = []
            for _ in range(3):
                val = int(hash_val % 256)
                hash_val = int(hash_val / 256)
                temp_list.append(val)
            temp_list.reverse()
            for val in temp_list:
                fp.write(struct.pack('B', val))
    fp.close()
    return

def main():
    hash_table = binary_reader()
    while True:
        ss = input('请输入功能：1：查询，2：插入，0：退出:\n')
        if ss == '1':
            input_str = input('请输入')
            if hash_str(input_str) in hash_table:
                print('exist')
            else:
                print('not exist')
        elif ss == '2':
            input_str = input('请输入')
            append_bin([hash_str(input_str)])
            print('添加成功')
        elif ss == '0':
            print('退出成功')
            break
        else:
            print('输入错误，请再次输入')
    return

if __name__ == '__main__':
    main()
    # df = pd.read_csv(r'/Users/liubenchen/Desktop/fuck_PY/test2/dataset.csv')
    pid = os.getpid()
    p = psutil.Process(pid)
    info = p.memory_full_info()
    print(info.uss / 1024. / 1024. / 1024.)
