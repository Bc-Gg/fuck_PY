from myfilter import *
from spyder import *
import pandas as pd
import queue
import threading
#===================  Global  =================
# query_queue = Queue()
query_queue = [] # url 的 请求队列
init_url = 'https://xmu.edu.cn/' # 一切罪恶的源头
query_queue.append(init_url)
# tel_filter = init_bloom(1e5) #初始化联系方式过滤器，貌似用不到
url_filter = init_bloom(2e7) #初始化url过滤器
url_list = [init_url] # debug模式中看看有哪些url我们曾经访问到过，实战中可以注释掉
tel_dict = {} # debug模式中看看我们都收集到了哪些联系方式。
#===================  Global  =================

def save_tel(org, temp_tel_list):
    '''
    将联系方式存储起来
    :param org: 联系人
    :param temp_tel_list: 联系方式
    :return: None
    '''
    if org in tel_dict.keys():
        tel_dict[org] = tel_dict[org] | set(temp_tel_list)
    else:
        tel_dict[org] = set(temp_tel_list)


def main():
    cnt = 0
    print('enter main')
    while len(query_queue) > 0:
        # 获取下一个要访问的url
        url = query_queue.pop(0)

        # 对url进行解析
        page = get_response(url)
        if not page == None:
            temp_url_list = get_url(page, url)
            org, temp_tel_list = get_info(page)
        else:
            temp_url_list = []
            org , temp_tel_list = None, []

        # 将联系当时存储起来
        if len(temp_tel_list) > 0:
            save_tel(org, temp_tel_list)
            print(org, temp_tel_list)

        # 将之后要访问的url储存起来
        for url in temp_url_list:
            if not url in url_filter:
                url_filter.add(url)
                query_queue.append(url)
                url_list.append(url)
        # 这里可以偷偷设置一下爬取次数，在debug的时候尽量不要爬取太多,实际应用可以直接关掉，
        # 因为当query_queue为空的时候会自动停止
        cnt += 1
        if cnt > 5000:
            break
    # print(url_list)
    print("======== Spyder part is done. Saving data as files ======")
    tel_dict.update((key, str(val)) for key ,val in tel_dict.items())
    df = pd.DataFrame(list(tel_dict.items()))
    df.to_csv(path_or_buf='dataset.csv',encoding='utf8')
    print(df)

def do_craw(url_queue:queue.Queue , html_queue: queue.Queue):
    while True:
        url = url_queue.get()
        page = get_response(url)
        html_queue.put((page,url))

def do_parse(url_queue:queue.Queue , html_queue: queue.Queue):
    while True:
        page, url = html_queue.get()
        if not page == None:
            temp_url_list = get_url(page, url)
            org, temp_tel_list = get_info(page)
        else:
            temp_url_list = []
            org , temp_tel_list = None, []

        # 将联系当时存储起来
        if len(temp_tel_list) > 0:
            save_tel(org, temp_tel_list)
            print(org, temp_tel_list)

        # 将之后要访问的url储存起来
        for url in temp_url_list:
            if not url in url_filter:
                url_filter.add(url)
                url_queue.put(url)
                url_list.append(url)


if __name__ == '__main__':
    url_queue = queue.Queue()
    html_queue = queue.Queue()
    url_queue.put(init_url)

    for idx in range(100):
        t = threading.Thread(target=do_craw , args=[url_queue, html_queue], name = f'craw No.{idx}')
        t.start()
    for idx in range(100):
        t = threading.Thread(target= do_parse, args=[url_queue, html_queue], name = f'parse No.{idx}')
        t.start()
