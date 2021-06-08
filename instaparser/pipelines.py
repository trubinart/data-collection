from pymongo import MongoClient
import hashlib
import json


class InstaparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client['instagram']

    def process_item(self, item, spider):
        collection_name = 'followers_and_following'
        try:
            collection = self.db.create_collection(f'{collection_name}')
        except:
            collection = self.db[collection_name]

        item_for_mongo_binary = json.dumps(dict(item)).encode('utf-8')
        hash = hashlib.sha3_256(item_for_mongo_binary)
        id = hash.hexdigest()
        item['_id'] = id

        try:
            collection.insert_one(item)

        except Exception:
            pass

        print('положили')
        return item