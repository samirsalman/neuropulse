import json
from typing import List
from src.data.generic_data import GenericData
from src.handlers.handler import Handler, HandlerMode
from pymongo import MongoClient
from src.app_logging.logger import logger


class MongoHandler(Handler):
    def __init__(
        self,
        name: str = None,
        mode: HandlerMode = HandlerMode.APPEND,
        mongo_host: str = None,
        mongo_user: str = None,
        mongo_password: str = None,
        mongo_db: str = None,
        mongo_collection: str = None,
        node_id: str = "node-0",
    ) -> None:
        super().__init__(name, mode)
        self.user = mongo_user
        self.password = mongo_password
        self.mongo_uri = mongo_host
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection
        self.client = MongoClient(
            self.mongo_uri,
            username=self.user,
            password=self.password,
        )
        try:
            self.client.server_info()
        except Exception as e:
            logger.error(f"Could not connect to mongo: {e}")
            raise e

        self.db = self.client[self.mongo_db]
        self.node_id = node_id

    def handle(self, data: List[GenericData]):
        logger.info(f"Saving {len(data)} data to mongo")
        _data = []
        for d in data:
            d = json.loads(d.to_json())
            d["index"] = self.db[self.mongo_collection].count_documents({})
            d["node_id"] = self.node_id
            _data.append(d)
        self.db[self.mongo_collection].insert_many(_data)
        logger.info(f"Saved {len(data)} data to mongo")

    def close(self):
        logger.info("Closing mongo connection")
        self.client.close()
        logger.info("Closed mongo connection")

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

    def clear(self):
        self.db[self.mongo_collection].delete_many({})
