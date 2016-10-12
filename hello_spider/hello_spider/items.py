# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PostItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    post_id = scrapy.Field()
    post_title = scrapy.Field()
    post_author_name = scrapy.Field()
    post_timestamp = scrapy.Field()
    post_latest_timestamp = scrapy.Field()
