# -*- coding = utf-8 -*-

from pybloom_live import ScalableBloomFilter, BloomFilter


def init_bloom(size=2e8):
    bloom = BloomFilter(capacity=size)
    return bloom


'''
def main():
    max_size = 20000000
    fp = open('data2.txt', 'r')
    bloom = ScalableBloomFilter(initial_capacity=max_size)
    for i in range(max_size):
        str = fp.readline()
        str = str.rstrip()
        bloom.add(str)
    fp.close()

    sstr = "###"
    while(True):
        choice = input("请输入要查询的字符串（输入“###”退出程序）：")
        if choice == sstr:
            break
        else:
            print(choice in bloom)

if __name__ == '__main__':
    main()

pid = os.getpid()
p = psutil.Process(pid)
info = p.memory_full_info()
'''
