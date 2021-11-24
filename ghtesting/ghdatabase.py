import pymongo
import logging as log

class GHDatabase:
    def __init__(self, db: str, collection: str, connectionString="mongodb://localhost:27017/"):
        self.client = pymongo.MongoClient(connectionString)
        self.db = self.client[db]
        if collection not in self.db.list_collection_names():
            self.db.create_collection(collection, capped=False) # unlimited documents
        self.col = self.db[collection]

    def update_repo(self, repojson):
        self.col.update_one({'_id': repojson['_id']}
                            , {'$set': repojson}
                            , upsert=True)

    def append_to_repo(self, name, jsondata):
        self.col.update_one({'_id': name}
                            , {'$set': jsondata}
                            , upsert=True)

    def repos_count(self):
        return self.col.count_documents({})

    def get_repos_by_name(self, name):
        return self.col.find({'_id': name})[0]

    def get_repos(self):
        return self.col.find({})

    def drop_database(self, dbname):
        self.client.drop_database(dbname)
