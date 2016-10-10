#!/usr/bin/env python
# coding=utf-8
import scrapy

from bs4 import BeautifulSoup


class DoubanPost(scrapy.Spider):
    name = 'douban_post'
    allowed_domains = ['douban.com']
    start_urls = [
        'http://www.douban.com/group/beijingzufang/discussion?start=0',
    ]

    def parse(self, response):
        print dir(response)
        soup = BeautifulSoup(reponse.text)
