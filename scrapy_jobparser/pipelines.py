# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import hashlib
import json
from pprint import pprint


class ScrapyJobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client['vacancy_db_2']

    def process_item(self, item, spider):
        collection_name = spider.name
        try:
            collection = self.db.create_collection(f'{collection_name}')
        except:
            collection = self.db[collection_name]

        vacancy_for_mongo_binary = json.dumps(dict(item)).encode('utf-8')
        hash = hashlib.sha3_256(vacancy_for_mongo_binary)
        id = hash.hexdigest()

        item['_id'] = id

        try:
            collection.insert_one(item)

        except Exception:
            pass

        return item
