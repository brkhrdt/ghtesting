import pymongo
import logging as log

class GHDatabase:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["github"]
        if 'repos' not in self.db.list_collection_names():
            self.db.create_collection('repos', capped=False) # unlimited documents
        self.col = self.db['repos']

    def update_repo(self, repojson):
        self.col.update_one({'_id': repojson['_id']}
                            , {'$set': repojson}
                            , upsert=True)

    def repos_count(self):
        return self.col.count_documents({})
