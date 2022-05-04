import queue
import threading

import pandas as pd

from myfilter import *
from spider import *

# ===================  Global  =================
# query_queue = Queue()
query_queue = []  # url 的 请求队列
init_url = 'https://xmu.edu.cn/'  # 一切罪恶的源头
query_queue.append(init_url)
# tel_filter = init_bloom(1e5) #初始化联系方式过滤器，貌似用不到
url_filter = init_static_bloom(20000)  # 初始化url过滤器 debug的时候要用定长，否则停不下来，也无法检验函数作用
# url_filter = init_scale_bloom(20)    # 初始化url过滤器，变长过滤器用于实际
url_list = [init_url]  # debug模式中看看有哪些url我们曾经访问到过，实战中可以注释掉所有相关变量
tel_dict = {}  # debug模式中看看我们都收集到了哪些联系方式。

# ===================  Global  =================

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


# def main():
#     '''
#     原始main函数
#     :return:
#     '''
#     cnt = 0
#     print('enter main')
#     while len(query_queue) > 0:
#         # 获取下一个要访问的url
#         url = query_queue.pop(0)
#
#         # 对url进行解析
#         page = get_response(url)
#         if not page == None:
#             temp_url_list = get_url(page, url)
#             org, temp_tel_list = get_info(page)
#         else:
#             temp_url_list = []
#             org , temp_tel_list = None, []
#
#         # 将联系当时存储起来
#         if len(temp_tel_list) > 0:
#             save_tel(org, temp_tel_list)
#             print(org, temp_tel_list)
#
#         # 将之后要访问的url储存起来
#         for url in temp_url_list:
#             if not url in url_filter:
#                 url_filter.add(url)
#                 query_queue.append(url)
#                 url_list.append(url)
#         # 这里可以偷偷设置一下爬取次数，在debug的时候尽量不要爬取太多,实际应用可以直接关掉，
#         # 因为当query_queue为空的时候会自动停止
#         cnt += 1
#         if cnt > 5000:
#             break
#     # print(url_list)
#     print("======== Spider part is done. Saving data as files ======")
#     tel_dict.update((key, str(val)) for key ,val in tel_dict.items())
#     df = pd.DataFrame(list(tel_dict.items()))
#     df.to_csv(path_or_buf='dataset.csv',encoding='utf8')
#     print(df)

def do_craw(url_queue: queue.Queue, html_queue: queue.Queue):
    while True:
        url = url_queue.get()
        # 观察线程状态
        # print(threading.current_thread().name, f"craw {url}")
        page = get_response(url)
        html_queue.put((page, url))
        if url_queue.empty():
            break


def do_parse(url_queue: queue.Queue, html_queue: queue.Queue):
    try:
        while True:
            page, url = html_queue.get()
            # 观察线程状态
            # print(threading.current_thread().name, f"parse {url}")
            if not page == None:
                temp_url_list = get_url(page, url)
                org, temp_tel_list = get_info(page)
            else:
                temp_url_list = []
                org, temp_tel_list = None, []

            # 将联系当时存储起来
            if len(temp_tel_list) > 0:
                save_tel(org, temp_tel_list)
                print(org, temp_tel_list)

            # 将之后要访问的url储存起来
            for url in temp_url_list:
                if not url in url_filter:
                    url_filter.add(url)
                    url_queue.put(url)
                    # url_list.append(url) # 可以被注释掉的变量
            if url_queue.empty():
                break
    except IndexError as e:
        print(e)
    finally:
        return


def init_msg_queue():
    '''
    初始化url_queue以及html_queue
    :return: url_queue, html_queue
    '''
    url_queue = queue.Queue()
    html_queue = queue.Queue()
    url_queue.put(init_url)
    return url_queue, html_queue


def start_threads(url_queue, html_queue, thread_num=10):
    '''
    启动线程函数，并返回线程列表
    :param url_queue: 需要访问的url所组成的队列
    :param html_queue: 需要解析的html文本所组成的队列
    :param thread_num: 启动的线程个数
    :return: 线程列表
    '''
    thread_list = []
    for idx in range(thread_num):
        t = threading.Thread(target=do_craw, args=[url_queue, html_queue], name=f'craw No.{idx + 1}')
        t.start()
        thread_list.append(t)
    for idx in range(thread_num):
        t = threading.Thread(target=do_parse, args=[url_queue, html_queue], name=f'parse No.{idx + 1}')
        t.start()
        thread_list.append(t)
    return thread_list


def save_as_csv(path='dataset.csv'):
    '''
    :param path: 保存文件路径，默认在当前文件夹下保存为'dataset.csv'
    :return: None
    '''
    print("======== Spider part is done. Saving data as files ======")
    tel_dict.update((key, str(val)) for key, val in tel_dict.items())
    df = pd.DataFrame(list(tel_dict.items()))
    df.to_csv(path_or_buf=path, encoding='utf8')
    print(df)


def main():
    url_queue, html_queue = init_msg_queue()
    thread_list = start_threads(url_queue=url_queue, html_queue=html_queue)
    for t in thread_list:  # 等待所有进程结束之后再做之后的事情
        t.join()
    save_as_csv()


if __name__ == '__main__':
    main()
