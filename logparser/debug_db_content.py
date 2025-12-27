import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
MONGO_DB = os.getenv("MONGODB_DB")

def list_recent_logs():
    print("🔍 Inspecting 'log' collection...")
    try:
        client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client[MONGO_DB]
        collection = db["log"]
        
        count = collection.count_documents({})
        print(f"Total Documents: {count}")
        
        if count == 0:
            print("⚠️ Collection is EMPTY. LogCollector hasn't saved anything yet.")
            return

        print("\nLast 5 Log Entries:")
        # Sort by _id descending (newest first)
        cursor = collection.find().sort("_id", -1).limit(5)
        
        for doc in cursor:
            run_id = doc.get("run_id", "N/A")
            log_len = len(doc.get("log_data", ""))
            print(f" - ID: {doc['_id']} | RunID: {run_id} | LogSize: {log_len} chars")

    except Exception as e:
        print(f"❌ DB Error: {e}")

if __name__ == "__main__":
    list_recent_logs()
