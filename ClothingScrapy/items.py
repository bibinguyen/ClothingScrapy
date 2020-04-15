# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class HMItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    productID = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()

class HMDetailItem(scrapy.Item):
    url = scrapy.Field()
    allIMG = scrapy.Field()
    description = scrapy.Field()
