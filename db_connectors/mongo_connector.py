import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os

def upload_csv_to_mongo(csv_path, db_name="mcp_project", collection_name="sales1"):
    try:
        # Load .env for Mongo URI
        load_dotenv(dotenv_path=".env")
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            raise Exception("❌ MONGO_URI not found in .env")

        # Read CSV
        df = pd.read_csv(csv_path)
        print("✅ CSV loaded successfully")

        # Connect to MongoDB Atlas
        client = MongoClient(mongo_uri)
        db = client["sales1_db"]
        collection = db["sales"]

        # Insert data
        records = df.to_dict(orient="records")
        collection.insert_many(records)
        print("✅ Data uploaded to MongoDB successfully")

    except Exception as e:
        print(f"❌ Upload failed: {e}")

# For direct testing
if __name__ == "__main__":
    upload_csv_to_mongo("csv_data/sales1.csv")

def get_mongo_data(db_name="sales1_db", collection_name="sales"):
    
    try:
        load_dotenv()
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            raise Exception("❌ MONGO_URI not found in .env")

        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]
        
        data = list(collection.find({}, {"_id": 0}))  # exclude MongoDB _id
        return data

    except Exception as e:
        print(f"❌ MongoDB fetch failed: {e}")
        return []
