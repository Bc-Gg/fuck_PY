from faker import Faker
import pandas as pd
# 命令行输入： pip install faker
fake = Faker()
def generate_data_set():
    ls = []
    for _ in range(10**7):
        # 这里填写字符长度
        ls.append(fake.pystr(min_chars=30, max_chars=30))
    df = pd.DataFrame(ls)
    df.to_csv(path_or_buf=r'dataset.csv',index=False)

def main():
    generate_data_set()

if __name__ == '__main__':
    main()