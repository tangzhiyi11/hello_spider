#!/usr/bin/env python
# coding=utf-8
import jieba
import jieba.analyse
import pymongo


db = pymongo.MongoClient('localhost', 27017)
db = db.douban


def analyze():
    result_dict = {}
    for doc in db.post.find({}):
        title = doc['post_title']
        seg_list = do_seg(title)
        for seg in seg_list:
            if result_dict.has_key(seg):
                result_dict[seg] += 1
            else:
                result_dict[seg] = 1
    result_list = sorted(result_dict.iteritems(), key=lambda d:d[1])
    for item in result_list:
        name = item[0]
        num = item[1]
        print name,'  ',str(num)
    print 'total len is %d' % len(result_list)


def do_seg(text):
    #seg_list = jieba.lcut_for_search(text)
    jieba.analyse.set_stop_words('stop_word.txt')
    tags = jieba.analyse.extract_tags(text)
    return tags


if __name__ == '__main__':
    analyze()
