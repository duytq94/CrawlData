import MySQLdb
import logging
from scrapy import Spider
from scrapy.selector import Selector
from trend.items import TrendItem
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, Join

# Use XPathItemLoader instead of normal to clean strange character in data result
class MyItemLoader(XPathItemLoader):
    default_item_class = TrendItem
    default_input_processor = MapCompose(lambda string: string.strip())
    default_output_processor = Join()


class MyTour(Spider):
    db = MySQLdb.connect("localhost", "root", "Tu0denchin_123", "chat_io")
    cursor = db.cursor()
    sql = 'SELECT link FROM list_link_trend WHERE from_website = "mytour"'
    cursor.execute(sql)
    results = cursor.fetchall()
    start_urls = []
    for link in results:
        start_urls.append(link[0])
    db.close()

    name = "mytour"
    # start_urls = ['https://mytour.vn/location/13221-du-lich-indonesia-thien-duong-cuc-hut-gioi-tre.html']
    def parse(self, response):
        loader = MyItemLoader(response=response)

        loader.add_xpath('title', '//div[@class="page-header"]/h1/text()')
        loader.add_xpath('intro', '//div[@class="detail-content col-xs-12 mg-bt-10"]/p/em/strong/text()')
        loader.add_xpath('content', '//div[@class="detail-content col-xs-12 mg-bt-10"]/p[@style="text-align: justify;"]/text()')
        loader.add_xpath('url', '//div[@class="detail-content col-xs-12 mg-bt-10"]/p[@style="text-align: center;"]/img/@src')
        loader.add_value('from_website', 'mytour')
        
        return loader.load_item()


class ivivu(Spider):
    db = MySQLdb.connect("localhost", "root", "Tu0denchin_123", "chat_io")
    cursor = db.cursor()
    sql = 'SELECT link FROM list_link_trend WHERE from_website = "ivivu"'
    cursor.execute(sql)
    results = cursor.fetchall()
    start_urls = []
    for link in results:
        start_urls.append(link[0])
    db.close()

    name = "ivivu"
    def parse(self, response):
        loader = MyItemLoader(response=response)

        loader.add_xpath('title', '//h1[@class="entry-title"]/text()')
        loader.add_xpath('intro', '//div[@class="entry-content"]/p[1]')
        loader.add_xpath('content', '//div[@class="entry-content"]')
        loader.add_value('from_website', 'ivivu')

        url = response.xpath('//div[@class="entry-content"]/p/img/@src').extract()
        if (url != []):
            loader.add_xpath('url', '//div[@class="entry-content"]/p/img/@src')
        else:
            loader.add_xpath('url', '//div[@class="entry-content"]/div/img/@src')

        return loader.load_item()