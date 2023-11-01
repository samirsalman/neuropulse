from typing import List
from src.data.generic_data import GenericData
from src.handlers.handler import Handler, HandlerMode
from pymongo import MongoClient


class MongoHandler(Handler):
    def __init__(
        self,
        name: str = None,
        mode: HandlerMode = HandlerMode.APPEND,
        mongo_uri: str = None,
        mongo_db: str = None,
        mongo_collection: str = None,
        node_id: str="node-0",
    ) -> None:
        super().__init__(name, mode)
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.node_id = node_id

    def handle(self, data: List[GenericData]):
        for d in data:
            d["index"] = self.db[self.mongo_collection].count_documents({})
            d["node_id"] = self.node_id
        self.db[self.mongo_collection].insert_many(data)

    def close(self):
        self.client.close()

    def get_all(self):
        return self.db[self.mongo_collection].find()

    def get_by_id(self, id: str):
        return self.db[self.mongo_collection].find_one({"_id": id})
    
    def get_last(self):
        return self.db[self.mongo_collection].find().sort([("_id", -1)]).limit(1)
    
    def get_last_n(self, n: int):
        return self.db[self.mongo_collection].find().sort([("_id", -1)]).limit(n)
        
    def get_index(self, index: int):
        return self.db[self.mongo_collection].find({"index": index})
    
    def get_by_node_id(self, node_id: str):
        return self.db[self.mongo_collection].find({"node_id": node_id})
    
    def get_by_query(self, query: dict):
        return self.db[self.mongo_collection].find(query)
    
    