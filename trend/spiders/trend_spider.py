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
    start_urls = ["https://www.ivivu.com/blog/2017/10/phat-hien-3-homestay-ngan-sao-moi-tinh-cuc-hot-o-da-lat/"]
    def parse(self, response):
        loader = MyItemLoader(response=response)
        loader.add_xpath('title', '//div[@class="entry-content"]/h2/text()')
        loader.add_xpath('content', '//div[@class="entry-content"]/p/text()')
        loader.add_xpath('url', '//div[@class="entry-content"]/div[@class="wp-caption aligncenter"]/img/@src')
        return loader.load_item()