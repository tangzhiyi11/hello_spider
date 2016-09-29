# -*- coding: utf-8 -*-
import zmq
import json
import sys

from douban import Post

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    context = zmq.Context()
    receiver = context.socket(zmq.PULL)
    receiver.bind('tcp://*:7776')
    post = Post()
    while True:
        msg = receiver.recv()
        item = json.loads(msg)
        post_latest_timestamp = int(item['post_latest_timestamp'])
        post.save_post_into_db(item, post_latest_timestamp)