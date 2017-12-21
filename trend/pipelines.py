# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import logging
from scrapy.exceptions import DropItem

class TrendPipeline(object):
    def process_item(self, item, spider):
        is_valid = True
        for data in item:
            if not data:
                is_valid = False
                raise DropItem("Missing %s!" % data)
        if is_valid:
            db = MySQLdb.connect("localhost", "root", "Tu0denchin_123", "chat_io")
            # save foreign character
            db.set_character_set('utf8')
            cursor = db.cursor()
            # save foreign character
            cursor.execute('SET NAMES utf8;')
            cursor.execute('SET CHARACTER SET utf8;')
            cursor.execute('SET character_set_connection=utf8;')
            sql = "INSERT INTO trend (title, intro, content, url, from_website, season, type) VALUES (%s, %s, %s, %s, %s, %s, %s)"
      

# -------------------------------------- Detect seaon ------------------------------------------------
            detectSpring = [u'mùa xuân', u'nhất trong năm', u'cuối năm', u'năm cũ', u'đầu năm', u'hoa mai', u'hoa đào', u'chợ hoa', u'trong trẻo', u'cờ đỏ', u'năm mới']
            detectSummer = [u'mùa hạ', u'hòn đảo', u'nắng nóng', u'bãi biển', u'bờ cát', u'bãi cát', u'mùa hè', u'nóng nực', u'hải sản', u'lặn', u'đại dương', u'cá biển', u'san hô', u'bơi lội']
            detectAutumn = [u'mùa thu', u'lá đỏ', u'lãng mạn', u'lá vàng', u'lá rụng', u'lá phong', u'nhẹ nhàng', u'dễ chịu', u'dịu nhẹ']
            detectWinter = [u'mùa đông', u'gió lạnh', u'băng tuyết', u'gió lùa', u'trà nóng', u'khăn choàng', u'áo len', u'áo ấm', u'co ro', u'lạnh giá', u'giá rét', u'sưởi ấm', u'áo khoác']

            currentSeason = -1
            countSpring = 0
            countSummer = 0
            countAutumn = 0
            countWinter = 0
            countMax = 0;

            for str in detectSpring:
                if (item["content"].find(str) != -1):
                    countSpring += 1
            if (countSpring > 0):
                countMax = countSpring
                currentSeason = 0

            for str in detectSummer:
                if (item["content"].find(str) != -1):
                    countSummer += 1
            if (countMax < countSummer):
                countMax = countSummer
                currentSeason = 1

            for str in detectAutumn:
                if (item["content"].find(str) != -1):
                    countAutumn += 1
            if (countMax < countAutumn):
                countMax = countAutumn
                currentSeason = 2

            for str in detectWinter:
                if (item["content"].find(str) != -1):
                    countWinter += 1
            if (countMax < countWinter):
                countMax = countWinter
                currentSeason = 3

# -------------------------------------- Detect type ------------------------------------------------
            currentType = -1
            countHighland = 0
            countBeach = 0
            countCity = 0
            countRiver = 0
            countMax = 0

            detectHighland = [u'cao nguyên', u'vùng núi', u'đồi chè', u'sườn đồi', u'thung lũng', u'sương sớm', u'lên cao', u'uốn lượn', u'tây bắc', u'đông bắc', u'mát lành', u'dãy núi', u'đường đèo', u'trên đèo', u'phố núi', u'núi rừng']
            detectBeach = [u'bãi biển', u'bờ cát', u'bãi cát', u'hải sản', u'thuyền buồm', u'bình minh', u'hòn đảo', u'làng chài', u'đại dương', u'biển trời', u'cát trắng', u'ghềnh đá', u'đánh bắt', u'chợ cá', u'gió biển', u'tiếng sóng']
            detectCity = [u'thành phố', u'xe cộ', u'kẹt xe', u'kinh tế', u'xã hội', u'quốc tế', u'sân bay', u'nhộn nhịp', u'sầm uất', u'mua sắm', u'đông đúc', u'hối hả', u'bận bịu', u'giới trẻ', u'thời trang', u'tấp nập', u'náo nhiệt']
            detectRiver = [u'miền tây', u'nước nổi', u'miệt vườn', u'đồng sen', u'đồng lúa', u'cánh cò', u'chợ nổi', u'sông nước', u'trái cây', u'tây nam bộ', u'rừng tràm']

            for str in detectHighland:
                if (item["content"].find(str) != -1):
                    countHighland += 1
            if (countMax < countHighland):
                countMax = countHighland
                currentType = 0

            for str in detectBeach:
                if (item["content"].find(str) != -1):
                    countBeach += 1
            if (countMax < countBeach):
                countMax = countBeach
                currentType = 1

            for str in detectCity:
                if (item["content"].find(str) != -1):
                    countCity += 1
            if (countMax < countCity):
                countMax = countCity
                currentType = 2

            for str in detectRiver:
                if (item["content"].find(str) != -1):
                    countRiver += 1
            if (countMax < countRiver):
                countMax = countRiver
                currentType = 3

# -------------------------------------- Write to database ------------------------------------------------

            arg = (item["title"], item["intro"], item["content"], item["url"], item["from_website"], currentSeason, currentType)
            cursor.execute(sql, arg)
            db.commit()
            db.close()
        return item
    pass