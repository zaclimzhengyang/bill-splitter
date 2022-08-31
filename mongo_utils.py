from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
mongo_client: MongoClient = MongoClient("mongodb://localhost:27017/")
db: Database = mongo_client.bill_splitter
users_collection: Collection = db.users
foods_collection: Collection = db.foods