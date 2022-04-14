import pandas as pd
import struct
import psutil
import os
MOD1 = 25165843

def reader():
    df = pd.read_csv(r'/Users/liubenchen/Desktop/fuck_PY/test2/dataset.csv')
    # df = pd.read_csv(r'/Users/liubenchen/Desktop/fuck_PY/test2/tempdataset.csv')
    return list(df.iloc[:,0])

def hash_str(ss):
    hash = 0
    for s in ss:
        hash = (hash * MOD1 + ord(s)) % 1e7
    return eval(hex(int(hash)))


def save_with_bin(hash_list):
    with open('hash_table.txt','wb') as fp:
        for hash_val in hash_list:
            print((hash_val))
            temp_list = []
            for _ in range(3):
                val = int(hash_val % 256)
                hash_val =int (hash_val / 256)
                temp_list.append(val)
            temp_list.reverse()
            for val in temp_list:
                fp.write(struct.pack('B',val))
    fp.close()
    return

def main():
    ll = reader()
    hash_list = [hash_str(ss) for ss in ll]
    save_with_bin(hash_list)
    return

if __name__ == '__main__':
    main()
    pid = os.getpid()
    p = psutil.Process(pid)
    info = p.memory_full_info()
    print(info.uss / 1024. / 1024. / 1024.)