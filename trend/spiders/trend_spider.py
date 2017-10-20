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


class TrendSpider(Spider):
    db = MySQLdb.connect("localhost", "root", "123456", "chat_io")
    cursor = db.cursor()
    sql = 'SELECT link FROM list_link_my_tour'
    cursor.execute(sql)
    results = cursor.fetchall()
    start_urls = []
    for link in results:
        start_urls.append(link[0])
    db.close()

    name = "trend"
    # start_urls = ['https://mytour.vn/location/13000-du-lich-nuoc-ngoai-dau-nam-tai-dai-loan-hong-kong.html']
    def parse(self, response):
        loader = MyItemLoader(response=response)
        loader.add_xpath('title', '//div[@class="page-header"]/h1/text()')
        loader.add_xpath('intro', '//div[@class="detail-content col-xs-12 mg-bt-10"]/p/em/strong/text()')
        loader.add_xpath('background', '//div[@class="detail-content col-xs-12 mg-bt-10"]/p[@style="text-align: center;"][1]/img/@src')
        loader.add_xpath('content', '//div[@class="detail-content col-xs-12 mg-bt-10"]/p[@style="text-align: justify;"]/text()')
        loader.add_xpath('url', '//div[@class="detail-content col-xs-12 mg-bt-10"]/p[@style="text-align: center;"]/img/@src')
        return loader.load_item()