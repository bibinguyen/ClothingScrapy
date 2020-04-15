# -*- coding: utf-8 -*-
import scrapy
from DatabaseExecute import GetCur
from SQLQueries import selectHM
from ..items import HMItem, HMDetailItem

class HMSpider(scrapy.Spider):
    name = "HM"
    allowed_domains = ["hm.com"]
    custom_settings = {
        "ITEM_PIPELINES": {
            "ClothingScrapy.pipelines.HMPipeline": 300
        }
    }
    
    pageSize = 100
    listURL = {
        "https://www2.hm.com/content/hmonline/en_us/women/products/dresses.html/": 0,
        "https://www2.hm.com/en_us/women/products/tops.html": 0,
        "https://www2.hm.com/en_us/women/products/shirts-blouses.html": 0,
        "https://www2.hm.com/en_us/women/products/cardigans-sweaters.html": 0,
        "https://www2.hm.com/en_us/women/products/pants.html": 0,
        "https://www2.hm.com/en_us/women/products/basics.html": 0,
        "https://www2.hm.com/en_us/women/products/hoodies-sweatshirts.html": 0,
        "https://www2.hm.com/en_us/women/products/blazers-vests.html": 0,
        "https://www2.hm.com/en_us/women/products/jackets-coats.html": 0,
        "https://www2.hm.com/en_us/women/products/jeans.html": 0,
        "https://www2.hm.com/en_us/women/products/skirts.html": 0,
        "https://www2.hm.com/en_us/women/products/shorts.html": 0,
        "https://www2.hm.com/en_us/women/products/jumpsuits-rompers.html": 0,
        "https://www2.hm.com/en_us/women/products/workout-clothes.html": 0,
        "https://www2.hm.com/en_us/women/products/maternity-clothes.html": 0,
        "https://www2.hm.com/en_us/women/products/plus-size.html": 0,
        "https://www2.hm.com/en_us/women/products/sleepwear-loungewear.html": 0,
        "https://www2.hm.com/en_us/women/products/petite.html": 0,
        "https://www2.hm.com/en_us/divided/products/tops.html": 0,
        "https://www2.hm.com/en_us/divided/products/basics.html": 0,
        "https://www2.hm.com/en_us/divided/products/jackets-coats.html": 0,
        "https://www2.hm.com/en_us/divided/products/shirts-and-blouses.html": 0,
        "https://www2.hm.com/en_us/divided/products/skirts.html": 0,
        "https://www2.hm.com/en_us/divided/products/jeans.html": 0,
        "https://www2.hm.com/en_us/divided/products/hoodies-sweatshirts.html": 0,
        "https://www2.hm.com/en_us/divided/products/shorts.html": 0,
        "https://www2.hm.com/en_us/divided/products/cardigans-sweaters.html": 0,
        "https://www2.hm.com/en_us/divided/products/dresses.html": 0,
        "https://www2.hm.com/en_us/divided/products/jumpsuits-rompers.html": 0,
        "https://www2.hm.com/en_us/divided/products/pants-leggings.html": 0,
        "https://www2.hm.com/en_us/men/products/hoodies-sweatshirts.html": 0,
        "https://www2.hm.com/en_us/men/products/t-shirts-tank-tops.html": 0,
        "https://www2.hm.com/en_us/men/products/basics.html": 0,
        "https://www2.hm.com/content/hmonline/en_us/men/products/shirts.html/": 0,
        "https://www2.hm.com/content/hmonline/en_us/men/products/jeans.html/": 0,
        "https://www2.hm.com/en_us/men/products/pants.html": 0,
        "https://www2.hm.com/en_us/men/products/jackets-coats.html": 0,
        "https://www2.hm.com/en_us/men/products/shorts.html": 0,
        "https://www2.hm.com/en_us/men/products/suits-blazers.html": 0,
        "https://www2.hm.com/en_us/men/products/cardigans-sweaters.html": 0,
        "https://www2.hm.com/en_us/men/products/nightwear-loungewear.html": 0,
        "https://www2.hm.com/en_us/men/products/sportswear.html": 0,
        "https://www2.hm.com/en_us/men/products/big-tall.html": 0,
    }
    
    def start_requests(self):
        for url in self.listURL:
            url = url + "?offset={}&page-size={}".format(self.listURL[url], self.pageSize)
            yield scrapy.Request(url = url, callback = self.Parse)
    
    def Parse(self, response):
        baseURL = response.url.split("?")[0]
        allCell = response.css("li.product-item")
        listGetID = allCell.css("article.hm-product-item").css("::attr(data-articlecode)").extract()
        
        
        for cell in allCell:
            item = HMItem()
            
            productID = cell.css("article.hm-product-item").css("::attr(data-articlecode)").extract_first()
            
            itemHeading = cell.css("h3.item-heading a")
            title = itemHeading.css("::text").extract_first()
            url = itemHeading.css("::attr(href)").extract_first()
            
            item["productID"] = productID
            item["url"] = url
            item["title"] = title
            item["source"] = response.url
            
            yield item
        
        numItems = int(response.css(".filter-pagination").css("::text").extract()[0].strip().split(" ")[0]) - self.pageSize
        while numItems > self.listURL[baseURL]:
            self.listURL[baseURL] += self.pageSize
            url = baseURL + "?offset={}&page-size={}".format(self.listURL[baseURL], self.pageSize)
            yield response.follow(url, callback = self.Parse)

class HMDetailSpider(scrapy.Spider):
    name = "HMDetail"
    allowed_domains = ["hm.com"]
    
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "ClothingScrapy.middlewares.HMDetailDownloaderMiddleware": 543,
        },
        "ITEM_PIPELINES": {
            "ClothingScrapy.pipelines.HMDetailPipeline": 300
        }
    }
    
    def start_requests(self):
        limit = getattr(self,"limit","all")
        
        conn, cur = GetCur()
        cur.execute(selectHM, (limit, ))
        hmData = cur.fetchall()
        conn.close()
        
        for data in hmData:
            productID = data[0]
            url = data[1]
            yield scrapy.Request(url = url, callback = self.Parse)
    
    def Parse(self, response):
        allIMG = response.css("figure.pdp-image img").css("::attr(src)").extract()
        title = response.css(".product-item-headline").css("::text").extract()[0]
        description = response.css(".product-input-label").css("::text").extract()[0]
        
        item = HMDetailItem()
        item["url"] = response.url
        item["allIMG"] = allIMG
        item["description"] = description
        
        yield item
