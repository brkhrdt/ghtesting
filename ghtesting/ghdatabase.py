import pymongo
import logging as log

class GHDatabase:
    def __init__(self, db: str, collection: str):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db]
        if collection not in self.db.list_collection_names():
            self.db.create_collection(collection, capped=False) # unlimited documents
        self.col = self.db[collection]

    def update_repo(self, repojson):
        self.col.update_one({'_id': repojson['_id']}
                            , {'$set': repojson}
                            , upsert=True)

    def repos_count(self):
        return self.col.count_documents({})
