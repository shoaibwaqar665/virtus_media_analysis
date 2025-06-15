from pymongo import MongoClient
import os
import dotenv
import json
import pandas as pd
from bson import json_util  # for ObjectId support
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


def get_signal_from_db():
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["virtusmediagroup"]
    collection = db['dev_signal']
    data = collection.find_one({})
    return data.get("scaper_signal") if data else None


def get_urls_from_db():
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["virtusmediagroup"]

    urls_collection = db['dev_test_urls']
    channels_collection = db['channels']

    # Get all existing URLs from channels
    existing_urls = set(
        doc['url'] for doc in channels_collection.find({"url": {"$exists": True}}, {"url": 1})
    )
    

    # Filter urls not already in channels
    result = {
        doc["platform"]: doc["url"]
        for doc in urls_collection.find({})
        if "platform" in doc and "url" in doc and doc["url"] not in existing_urls
    }

    return result



# get all data from channels collection and convert it into JSON and CSV and make it downloadable

def get_all_data_from_channels():
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["virtusmediagroup"]
    collection = db['channels']
    data = list(collection.find({}))  # Convert cursor to list
    return data


def save_data_to_files():
    # Get data
    data = get_all_data_from_channels()

    # ✅ Save as JSON (handles ObjectId correctly)
    with open('channels_data.json', 'w', encoding='utf-8') as f:
        f.write(json_util.dumps(data, indent=4, ensure_ascii=False))

    # ✅ Save as CSV
    df = pd.DataFrame(data)
    df.drop(columns=["_id"], inplace=True, errors='ignore')  # Optional: drop Mongo _id
    df.to_csv('channels_data.csv', index=False)
