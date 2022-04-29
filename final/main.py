from myfilter import *
from spyder import *
from queue import Queue

# query_queue = Queue()
query_queue = []
init_url = 'https://xmu.edu.cn/'
query_queue.append(init_url)
tel_filter = init_bloom(1e5)
url_filter = init_bloom(1e5)
url_list = [init_url]

def main():
    print('enter main ')
    while len(query_queue) > 0:
        url = query_queue.pop(0)
        page = analysis_page(url)
        temp_url_list = get_url(page, url)
        print(temp_url_list)
        # temp_tel_list = get_info(page)
        for url in temp_url_list:
            if not url in url_filter:
                print(url)
                url_filter.add(url)
                query_queue.append(url)
                url_list.append(url)
    print(url_list)



if __name__ == '__main__':
    main()
