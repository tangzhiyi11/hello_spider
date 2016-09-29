# -*- coding: utf-8 -*-
import requests
import zmq
import sys
import ConfigParser
import re
import time

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


class Master:
    def __init__(self):
        self.context = zmq.Context()
        self.sender = self.context.socket(zmq.PUSH)
        self.sender.bind('tcp://*:7777')
        self.url_seed = []

    def parse_config(self, file_name='url_params.conf'):
        conf = ConfigParser.ConfigParser()
        with open(file_name) as input_file:
            conf.readfp(input_file)
            for section in conf.sections():
                self.url_seed.append(conf.get(section, 'url'))

    def do_spider(self):
        self.parse_config()
        urls = self.get_html_increase(self.url_seed)
        for url in urls:
            html = requests.get(url, headers=headers, verify=False)
            if int(html.status_code) != 200:
                print 'parse_url %s failed! status_code: %s' % (url, html.status_code)
            result = self.get_urls_from_html(html.text)
            for post in result:
                post_id = post[0]
                latest_time = str(post[1])
                self.sender.send(post_id+' '+latest_time)
                print "processing %s" % post_id
                time.sleep(4)

    def get_html_increase(self, url_list):
        for url in url_list:
            i = 0
            while i <= 359050:
                this_url = url + str(i)
                i += 25
                yield this_url


    def get_urls_from_html(self, html):
        try:
            soup = BeautifulSoup(html, "lxml")
            tr_list = soup.find_all('tr', attrs={'class': ''})
            for tr in tr_list:
                if not tr.has_attr('class'):
                    continue
                # get url
                title_td = tr.find('td', attrs={'class': 'title'})
                url = title_td.find('a')['href']
                post_id = self.get_post_id_from_url(url)
                # print post_id
                # get latest time
                time_td = tr.find('td', attrs={'class': 'time'})
                latest_time = self.get_timestamp(time_td.text)
                # print latest_time
                yield (post_id, latest_time)
        except:
            pass

    def get_timestamp(self, latest_time):
        if re.match(r'^\d{2}.*', latest_time) == None:
            time_array = time.strptime(latest_time, '%Y-%m-%d')
        else:
            time_array = time.strptime('2016-' + latest_time, '%Y-%m-%d %H:%M')
        timestamp = int(time.mktime(time_array))
        return timestamp

    def get_post_id_from_url(slef, url):
        if not url.endswith('/'):
            url += '/'
        return url.split('/')[-2]

if __name__ == '__main__':
    spider = Master()
    while True:
        spider.do_spider()
