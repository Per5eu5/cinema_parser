# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Parser3Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()
    title = scrapy.Field()
    age = scrapy.Field()
    start_times = scrapy.Field()
    dimensions = scrapy.Field()
    halls = scrapy.Field()
    poster = scrapy.Field()
    date = scrapy.Field()


class Detail(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    cost = scrapy.Field()
    date = scrapy.Field()

    age = scrapy.Field()

    url = scrapy.Field()
    start_time = scrapy.Field()
    dimension = scrapy.Field()
    hall = scrapy.Field()
    poster = scrapy.Field()


