# -*- coding: utf-8 -*-
import requests
import zmq
import sys

from bs4 import BeautifulSoup
from douban import Post

reload(sys)
sys.setdefaultencoding('utf-8')

headers = {
    'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/27.0.1453.93',
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Host' : 'www.douban.com',
    'Accept-Language' : 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
    'Accept-Encoding' : 'gzip, deflate, br'
}

class master:
    def __init__(self)
