# 超级多的数据存储器
## 实现方法
1. 直接用pandas （300MB）
2. 把字符哈希到三个byte的长度，然后写成二进制 （60-70MB）
3. bloom filter （甚至可以几MB）
## 1 这种直接调库没写,Baidu一下就行了
## 2 哈希值十六进制存储
step1 generate_data.py  
step2 binary_writer.py  
step3 binary_reader.py  
**缺点**  
冲突概率非常大  
**改进**  
双哈希+bitset优化
## 3 手撸bloom
### 实现1 package_bloom.py 
### 实现2 my_bloom.py 