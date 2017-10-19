# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from scrapy.exceptions import DropItem

class TrendPipeline(object):
    def process_item(self, item, spider):
        is_valid = True
        for data in item:
            if not data:
                is_valid = False
                raise DropItem("Missing %s!" % data)
        if is_valid:
            db = MySQLdb.connect("localhost", "root", "123456", "chat_io")
            # save foreign character
            db.set_character_set('utf8')
            cursor = db.cursor()
            # save foreign character
            cursor.execute('SET NAMES utf8;')
            cursor.execute('SET CHARACTER SET utf8;')
            cursor.execute('SET character_set_connection=utf8;')
            sql = "INSERT INTO trend (title, intro, content, url) VALUES (%s, %s, %s, %s)"
            arg = (item["title"], item["intro"], item["content"], item["url"])
            cursor.execute(sql, arg)
            db.commit()
            db.close()
        return item
    pass