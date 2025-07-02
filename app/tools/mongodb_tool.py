from pymongo import MongoClient
from crewai.tools.base_tool import BaseTool
from pydantic import PrivateAttr

class MongoDBTool(BaseTool):
    name: str = "MongoDBTool"
    description: str = "Tool for interacting with MongoDB for client and payment data."
    _client: MongoClient = PrivateAttr()
    _db: object = PrivateAttr()

    def __init__(self, uri, db_name, **data):
        super().__init__(**data)
        self._client = MongoClient(uri)
        self._db = self._client[db_name]
        print("Here-----------------------------------")
        print(self._db.list_collection_names())
    
    def find_client(self, query):
        return self._db.clients.find_one(query)
    
    def aggregate_revenue(self, start_date, end_date):
        pipeline = [
            {"$match": {"payment_date": {"$gte": start_date, "$lte": end_date}}},
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ]
        return list(self._db.payments.aggregate(pipeline))

    def get_classes_for_week(self, start_date, end_date):
        query = {
            "date": {"$gte": start_date, "$lte": end_date}
        }
        print(list(self._db.classes.find(query)))
        return list(self._db.classes.find(query))

    def run(self, action, *args, **kwargs):
        # Example run method for CrewAI compatibility
        if action == "find_client":
            return self.find_client(*args, **kwargs)
        elif action == "aggregate_revenue":
            return self.aggregate_revenue(*args, **kwargs)
        elif action == "get_classes_for_week":
            return self.get_classes_for_week(*args, **kwargs)
        else:
            return f"Unknown action: {action}"

    def _run(self, *args, **kwargs):
        return self.run(*args, **kwargs)