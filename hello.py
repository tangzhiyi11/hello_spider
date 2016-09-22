import requests
import ConfigParser
import argparse
import pickle
import sys
import time
import re

from bs4 import BeautifulSoup
from douban import Post

reload(sys)
sys.setdefaultencoding('utf-8')


urls = []
result_list = []

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Host': "www.douban.com",
    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
}

class douban_spider:

    def __init__(self, fun):
        self.urls = []
        self.url_seed = []
        self.url_gen_fun = fun
        self.post_result = []

    def do_spider(self):
        self.parse_config()
        self.gen_urls()
        #print self.urls
        self.parse_urls()
        #print self.post_result

    def parse_config(self, file_name='url_params.conf'):
        conf = ConfigParser.ConfigParser()
        with open(file_name) as input_file:
            conf.readfp(input_file)
            for section in conf.sections():
                self.url_seed.append(conf.get(section, 'url'))

    def gen_urls(self):
        self.urls = self.url_gen_fun(self.url_seed)

    def parse_urls(self):
        for url in self.urls:
            self.parse_url(url)

    def parse_url(self, url):
        html = requests.get(url, headers=headers, verify=False)
        if int(html.status_code) != 200:
            print 'parse_url %s failed! status_code: %s' % (url, html.status_code)
        result = self.get_urls_from_html(html.text)
        self.post_result.extend(result)
        post = Post()
        for item in self.post_result:
            post_id = item[0]
            latest_timestamp = item[1]
            result_post = post.parse_post(post_id)
            if not result_post:
                print "parse failed!"
                print post_id
                print latest_timestamp
                continue
            post.save_post_into_db(result_post, latest_timestamp)
            time.sleep(5)
        self.post_result= []

    def get_urls_from_html(self, html):
        soup = BeautifulSoup(html)
        tr_list = soup.find_all('tr',attrs={'class':''})
        result_urls = []
        for tr in tr_list:
            if not tr.has_attr('class'):
                continue
            #get url
            title_td = tr.find('td', attrs={'class' : 'title'})
            url = title_td.find('a')['href']
            post_id = self.get_post_id_from_url(url)
            #print post_id
            #get latest time
            time_td = tr.find('td', attrs={'class' : 'time'})
            latest_time = self.get_timestamp(time_td.text)
            #print latest_time
            result_urls.append((post_id, latest_time))
        return result_urls

    def get_timestamp(self, latest_time):
        if re.match(r'^\d{2}.*', latest_time) == None:
            time_array = time.strptime(latest_time, '%Y-%m-%d')
        else:
            time_array = time.strptime('2016-'+latest_time, '%Y-%m-%d %H:%M')
        timestamp = int(time.mktime(time_array))
        return timestamp

    def get_post_id_from_url(slef, url):
        if not url.endswith('/'):
            url += '/'
        return url.split('/')[-2]


def get_html_increase(url_list):
    result = []
    for url in url_list:
        i = 0
        while i <= 359050:
            this_url = url + str(i)
            i += 25
            result.append(this_url)
    return result


if __name__ == '__main__':
    spider = douban_spider(get_html_increase)
    spider.do_spider()

