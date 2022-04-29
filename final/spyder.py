import requests as rq
from bs4 import BeautifulSoup as bs
from restr import *


def analysis_page(url):
    try:
        res = rq.request(url=url, method='get')
        res.raise_for_status()
        # res.encoding = chardet.detect(res.content).get('encoding')
        res.encoding = res.apparent_encoding
        return res
    except:
        print(f'this {url} is dead')
        return None


def get_base_url(url):
    regex_exp = r'(?<=://)[a-zA-Z\.0-9]+(?=\/)'
    baseurl = re.findall(regex_exp, url, re.U)
    if baseurl:
        return baseurl[0]
    return None


def get_info(page):
    if page == None:
        return None, []
    page = bs(page.content, 'html.parser')
    content = str(page)
    org = find_org(content)
    tel_list = find_tel(content)
    return org, tel_list


def get_url(page, url):
    try:
        # print(url)
        baseurl = get_base_url(url)
        if page == None or baseurl == None:
            return []
        baseurl = 'https://' + baseurl + '/'
        soup = bs(page.content, 'html.parser')
        tags = soup.select("a")
        ans = set()
        for a in tags:
            if not a.get('href') == None:
                context = str(a['href'])
                if context.endswith('.htm') and not context.startswith('http'):
                    ans.add(baseurl + a['href'])
                elif context.__contains__('xmu.edu.cn') and not context.endswith('pdf'):
                    ans.add(a['href'])
        return ans
    except KeyError as ke:
        print(f'{url} do not has key {ke}')
        return None