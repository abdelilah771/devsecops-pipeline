
from pymongo import MongoClient
from app.config import settings

def debug_check():
    client = MongoClient(settings.mongo_uri)
    db = client[settings.mongo_db]
    logs_col = db["Log"]
    
    print(f"Checking DB: {settings.mongo_db}, Collection: Log")
    count = logs_col.count_documents({})
    print(f"Total Logs: {count}")
    
    docs = list(logs_col.find({"run_id": "test_auto_run_001"}))
    print(f"Found {len(docs)} docs with run_id=test_auto_run_001")
    for doc in docs:
        print(doc)

if __name__ == "__main__":
    debug_check()
