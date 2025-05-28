from pymongo import MongoClient
import os
import dotenv

dotenv.load_dotenv()

def store_data_in_db(data):
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["virtusmediagroup"]
    collection = db['channels']
    if isinstance(data, list):
        collection.insert_many(data)
    else:
        collection.insert_one(data)
    print(f"✅ Data inserted into channels collection successfully.")
