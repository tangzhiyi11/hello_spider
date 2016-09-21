# -*- coding: utf-8 -*-
import auth
import requests
import re
import time
import cgi
import HTMLParser

from bs4 import BeautifulSoup
from pymongo import MongoClient

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Host': "www.douban.com",
    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
}
db = MongoClient('localhost', 27017)
douban_db = db['douban']


class Post:
    def __init__(self, auth_flag=False):
        self.base_url = 'https://www.douban.com/group/topic/'
        self.auth_flag = auth_flag
        self.post_db = douban_db['post']
        if self.auth_flag:
            (account, password) = auth.Auth.parse_conf()
            if not account or not password:
                print 'input account and password!'
            self.douban_login = auth.Auth(account, password)
            self.douban_login.login()
        else:
            self.douban_login = None

    def get_post_html(self, post_id, auth_flag=False):
        url = self.base_url + post_id + '/'
        if auth_flag and auth_flag:
            response = self.douban_login.url_get(url)
            if int(response.status_code) != 200:
                print 'get post html failed!'
                return None
            else:
                return response.text
        else:
            response = requests.get(url, headers=headers, verify=False)
            if int(response.status_code) != 200:
                print 'get post html failed!'
                return None
            else:
                return response.text

    def parse_post(self, post_id):
        html = self.get_post_html(post_id)
        post = self.parse_post_html(html)
        post['post_id'] = post_id
        return post

    def parse_post_html(self, html):
        soup = BeautifulSoup(html)
        post_title = soup.find('title').text.strip()
        topic_doc = soup.find('div', attrs={'class':'topic-doc'})
        post_author_a = topic_doc.find('span', attrs={'class':'from'}).find('a')
        post_author_name = post_author_a.text.strip()
        post_author_uid = post_author_a['href'].split('/')[-2]
        post_time = topic_doc.find('h3').find('span', attrs={'class':'color-green'}).text.strip()
        time_array = time.strptime(post_time, '%Y-%m-%d %H:%M:%S')
        post_timestamp = int(time.mktime(time_array))
        post_content = topic_doc.find('div', attrs={'class':'topic-content'}).text
        post_content = cgi.escape(post_content)
        self.test_result(post_content)
        post_dict = {
            'post_title' : post_title,
            'post_author_name' : post_author_name,
            'post_author_uid' : post_author_uid,
            'post_timestamp' : post_timestamp,
            'post_content' : post_content
        }
        return post_dict

    def save_post_into_db(self, post_dict, latest_timestamp):
        post_id = post_dict['post_id']
        post_dict['post_latest_timestamp'] = latest_timestamp
        query_result = self.post_db.find_one({'post_id':post_id})
        if query_result:
            print 'post_id already exsited!'
            result = self.post_db.find_one_and_replace({'post_id':post_id},post_dict)
            print 'find and replaced! '
        else:
            print 'post_id not exsited!'
            result = self.post_db.insert_one(post_dict)
            print 'inserted_id is ',str(result.inserted_id)


    def test_result(self, result):
        with open('result.txt', 'w') as result_file:
            result_file.write(result)


if __name__ == '__main__':
    latest_timestamp = 1473491561
    post = Post()
    result = post.parse_post('90692347')
    post.save_post_into_db(result, latest_timestamp)

