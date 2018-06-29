# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ZuFangItem(scrapy.Item):
    # 该房源名称
    name = scrapy.Field()
    url = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 楼层
    floor = scrapy.Field()
    # 房屋户型
    apartments = scrapy.Field()
    # 房屋朝向
    towards = scrapy.Field()
    # 地铁
    subway = scrapy.Field()
    # 小区
    microdistrict = scrapy.Field()
    # 位置
    location = scrapy.Field()
    # 经纪人
    broker = scrapy.Field()
    broker_phone = scrapy.Field()
    # 城市
    city = scrapy.Field()
