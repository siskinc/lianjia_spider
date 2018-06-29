# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from lianjia.settings import MONGO_COLLECTION, MONGO_HOST, MONGO_PORT

class LianjiaPipeline(object):
    def __init__(self, *args, **kwargs):
        client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
        lianjia_db = client.lianjia
        self.zu_fang = lianjia_db.zu_fang
    def process_item(self, item, spider):
        self.zu_fang.update({'url': item['url']},
        {
            "$setOnInsert":
                {
                    'name': item['name'],
                    'price': item['price'],
                    'area': item['area'],
                    'floor': item['floor'],
                    'apartments': item['apartments'],
                    'towards': item['towards'],
                    'subway': item['subway'],
                    'microdistrict': item['microdistrict'],
                    'location': item['location'],
                    'broker': item['broker'],
                    'broker_phone': item['broker_phone'],
                    'city': item['city'],
                },
        }, upsert=True)
        print("保存 %s %s " % (item['city'], item['name']))
        return item
