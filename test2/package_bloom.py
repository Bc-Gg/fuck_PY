from pybloom_live import ScalableBloomFilter
import os
import psutil

class Bloom:
    def __init__(self):
        self.bloom = ScalableBloomFilter(initial_capacity=1e+7,error_rate=0.01)
        with open('data.txt','r') as f:
            while True:
                line = f.readline()
                line = line.rstrip()
                if not line:
                    break
                self.bloom.add(line)
        print ('内存使用：',psutil.Process(os.getpid()).memory_info().rss/1024/1024 , 'MB')

    def find_key(self,key:str):
        with open('data.txt','a') as f:
            if key in self.bloom:
                print("the key {} exists".format(key))
                return True
            else:
                print(("the key {} does not exists".format(key)))
                self.bloom.add(key)
                f.write(key+"\n")
                return False

sql=Bloom()
while True:
    order=int(input())
    if order == 1:
        key=input("输入要查询的键\n")
        print(sql.find_key(key))
    elif order == 2:
        break
    elif order == 3:
        pid = os.getpid()
        p = psutil.Process(pid)
        info = p.memory_full_info()
        print(info.uss/1024./1024./1024.)
    else:
        print("重新输入")
pid = os.getpid()
p = psutil.Process(pid)
info = p.memory_full_info()
print(info.uss/1024./1024./1024.)