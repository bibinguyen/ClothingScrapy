# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from DatabaseExecute import GetCur
from SQLQueries import insertHM, insertHMDetail, updateHM

class HMPipeline(object):
    
    def open_spider(self, spider):
        self.connection, self.cur = GetCur()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()
    
    def process_item(self, item, spider):
        productID = item["productID"]
        url = "https://www2.hm.com" + item["url"]
        title = item["title"].strip()
        source = item["source"]
        
        hmData = (productID, url, title, None, False, source)
        self.cur.execute(insertHM, hmData)

        return item

class HMDetailPipeline(object):
    
    def open_spider(self, spider):
        self.connection, self.cur = GetCur()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()
    
    def process_item(self, item, spider):
        url = item["url"]
        allIMG = item["allIMG"]
        description = item["description"].strip()
        
        productID = url.split(".")[-2]
        
        for img in allIMG:
            hmDetailData = (productID, "https:" + img)
            self.cur.execute(insertHMDetail, hmDetailData)
        
        newHMData = (description, True, productID)
        self.cur.execute(updateHM, newHMData)
        
        return item
