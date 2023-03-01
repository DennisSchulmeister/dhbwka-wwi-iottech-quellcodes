import pymongo
from pymongo import MongoClient
from typing import Dict, List
from os import getenv


def get_connection() -> MongoClient: 
    return pymongo.MongoClient(getenv('MONGO_DB_CONNECTION'))


def insert_document(client, collection_name: str, data_list : List[Dict]):
    db = client.get_database('sensor_db')
    collection = db.get_collection(collection_name)
    collection.insert_many(data_list)
