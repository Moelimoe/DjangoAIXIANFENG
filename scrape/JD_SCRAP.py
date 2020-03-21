from bs4 import BeautifulSoup
from urllib.request import urlopen
import re


# 页码page= 1、3、5、7.....
# 页码s = 1、53、104、156
html = urlopen('')


# import requests
# heads = {}
# heads['User-Agent'] = 'Mozilla/5.0 ' \
#                       '(Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 ' \
#                       '(KHTML, like Gecko) Version/5.1 Safari/534.50'
# response = requests.get('http://www.baidu.com', headers=headers)


import requests
import re

def get_html(url):
    proxy = {
        'http': '120.25.253.234:812',
        'https': '163.125.222.244:8123'
    }
    heads = {}
    heads['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
    req = requests.get(url, headers=heads, proxies=proxy)
    html = req.text
    return html

import requests
url = 'https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg'
# 这是那个，请求歌曲评论的url
headers = {
    'origin': 'https://y.qq.com',
    # 请求来源，本案例中其实是不需要加这个参数的，只是为了演示
    'referer': 'https://y.qq.com/n/yqq/song/004Z8Ihr0JIu5s.html',
    # 请求来源，携带的信息比“origin”更丰富，本案例中其实是不需要加这个参数的，只是为了演示
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    # 标记了请求从什么设备，什么浏览器上发出
}
params = {...}
res_music = requests.get(url, headers=headers, params=params)
# 发起请求
