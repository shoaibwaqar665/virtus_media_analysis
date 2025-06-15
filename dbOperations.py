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


def get_signal_from_db():
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["virtusmediagroup"]
    collection = db['dev_signal']
    data = collection.find_one({})
    return data.get("scaper_signal") if data else None


def get_urls_from_db():
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["virtusmediagroup"]
    collection = db['dev_test_urls']
    
    # Get all documents and extract platform + url
    documents = collection.find({})
    result = {
        doc["platform"]: doc["url"]
        for doc in documents
        if "platform" in doc and "url" in doc
    }
    
    return result

if __name__ == "__main__":
    print(get_urls_from_db())
