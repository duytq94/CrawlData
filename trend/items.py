# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TrendItem(scrapy.Item):
    title = scrapy.Field()
    intro = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    from_website = scrapy.Field()