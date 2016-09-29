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

class Worker:
    def __init__(self):
        self.context = zmq.Context()
        self.receiver = self.context.socket(zmq.PULL)
        self.receiver.connect("tcp://localhost:7777")
        self.post = Post()

    def do_parse(self):
        msg = self.receiver.recv()
        print "msg from worker: %s" % msg
        post_id, post_latest_timestamp = self.parse_msg(msg)
        try:
            result_post = self.post.parse_post(post_id)
            if not result_post:
                print "parse failed!"
                print post_id
                print post_latest_timestamp
            else:
                print result_post
        except:
            print "parse failed!"
        time.sleep(5)

    def parse_msg(self, msg):
        msg = msg.strip().split(' ')
        post_id = msg[0]
        post_latest_timestamp = msg[1]
        return post_id, post_latest_timestamp

if __name__ == '__main__':
    worker = Worker()
    while True:
        worker.do_parse()
