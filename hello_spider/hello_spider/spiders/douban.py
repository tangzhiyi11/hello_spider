# -*- coding:utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from ..items import HelloSpiderItem


class DoubanPost(CrawlSpider):
    name = "douban"
    download_delay = 5