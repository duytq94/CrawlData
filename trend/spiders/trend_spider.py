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
    name = "trend"
    start_urls = ["https://mytour.vn/location/13174-giac-mo-da-lat-cua-mot-co-gai.html",
    "https://mytour.vn/location/13171-du-lich-kham-pha-chinh-phuc-cuc-dong.html",]
    def parse(self, response):
        loader = MyItemLoader(response=response)
        loader.add_xpath('title', '//div[@class="page-header"]/h1/text()')
        loader.add_xpath('intro', '//div[@class="detail-content col-xs-12 mg-bt-10"]/p[1]')
        loader.add_xpath('background', '//div[@class="detail-content col-xs-12 mg-bt-10"]/p[@style="text-align: center;"][1]/img/@src')
        loader.add_xpath('content', '//div[@class="detail-content col-xs-12 mg-bt-10"]/p[@style="text-align: justify;"]/text()')
        loader.add_xpath('url', '//div[@class="detail-content col-xs-12 mg-bt-10"]/p[@style="text-align: center;"]/img/@src')
        return loader.load_item()