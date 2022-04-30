import chardet
import requests as rq
from bs4 import BeautifulSoup as bs
from restr import *


def get_response(url):
    '''
    本函数用来对url发起get请求并且针对网页对应编码进行解析, 如果url挂掉了返回None    \n
    但是会有特殊空格符的编码错误问题 可以参考网址：https://www.cnblogs.com/ArdenWang/p/15346276.html \n
    针对编码问题可以使用chardet来解决（好像不用也可以
    :param url: 输入一个url
    :return: obj: requests.response
    '''
    try:
        response = rq.request(url=url, method='get',timeout=1)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        if not response == None:
            return bs(response.content,'lxml')
        return response
    except:
        print(f'this {url} is dead, jump over it')
        return None


def get_base_url(url):
    '''
    get domain
    :param url:
    :return: If it has return domain url ,else return None
    '''
    regex_exp = r'(?<=://)[a-zA-Z\.0-9]+(?=\/)'
    baseurl = re.findall(regex_exp, url, re.U)
    if baseurl:
        return baseurl[0]
    return None


def get_info(page):
    '''
    通过作业1的方法获取org和tel
    :param page: requests.response 的对象
    :return: tuple(org, tel_list)
    '''
    content = str(page)
    org = find_org(content)
    tel_list = find_tel(content)
    tel_list = [tel.replace(u'\xa0',u'') for tel in tel_list]
    return org, tel_list


def get_url(soup, url):
    '''
    从一个请求中获取其页面中所有超链接并且保存
    :param page: 一个 requests.response 对象
    :param url:  page对象的url，为了获取其域名
    :return: 如果没有错误，就会返回正常的url的集合，否则抛出错误并返回None
    '''
    try:
        # print(url)
        baseurl = get_base_url(url)
        if baseurl == None:
            return []
        baseurl = 'https://' + baseurl + '/'
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