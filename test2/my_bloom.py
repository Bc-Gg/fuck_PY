import random
from bitarray import bitarray
import os.path
import psutil


# bitarray长度
BIT_SIZE = int(8e8+10)

class BloomFilter():

  def __init__(self):
    bit_array = bitarray(BIT_SIZE)
    bit_array.setall(0)
    self.bit_array = bit_array
    self.bit_size = self.length()
    self.cnt = 0

  def get_points(self, key):
    point_list = []
    for i in range(7):
      point = hash(key) % self.bit_size
      point_list.append(point)
    return point_list


  def contains(self, key):
    points = self.get_points(key)
    for p in points:
      if self.bit_array[p] == 0:
        return False
    return True

  def add(self, key):
    res = self.bitarray_expand()
    points = self.get_points(key)
    try:
      if self.contains(key):
        self.cnt += 1
      for point in points:
        self.bit_array[point] = 1
      return "添加完成！"
    except Exception as e:
      return e

  def count(self):
    return self.bit_array.count()

  def length(self):
    return len(self.bit_array)


  def bitarray_expand(self):
    """
    扩充bitarray长度
    """
    isusespace = round(int(self.count()) / int(self.length()),4)
    if 0.50 < isusespace:
      # 新建bitarray
      expand_bitarray = bitarray(BIT_SIZE)
      expand_bitarray.setall(0)
      # 增加新建的bitarray
      self.bit_array = self.bit_array + expand_bitarray
      self.bit_size = self.length()
      return self.bit_size
    else:
      return f"长度还够用,{round(isusespace * 100,2)}%"



def get_captcha():
  """
  生成用于测试的随机码
  :return:
  """
  seed = "abcdefghijklmnopqrstuvwxyz"
  captcha = ""
  for i in range(30):
    captcha += random.choice(seed)
  print(captcha)
  return captcha


if __name__ == "__main__":
  bloom = BloomFilter()
  for i in range(100):
    bloom.add(get_captcha())
    # print(bloom.length())
    # print(bloom.count())
  print("chongfugeshu:",bloom.cnt)
  while True:
    order = int(input('请输入编码'))
    if order == 1:
      key = input("输入要查询的键\n")
      print(bloom.contains(key))
    elif order == 2:
      key = input("输入要添加的键\n")
      bloom.add(key)
    elif order == 3:
      break
    else:
      print("重新输入")
  pid = os.getpid()
  p = psutil.Process(pid)
  info = p.memory_full_info()
  print(info.uss / 1024. / 1024. / 1024.)