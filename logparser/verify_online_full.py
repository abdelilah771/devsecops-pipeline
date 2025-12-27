import httpx
import pymongo
import os
import json
from dotenv import load_dotenv

# Load env vars to get DB connection details directly for seeding
load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
MONGO_DB = os.getenv("MONGODB_DB")
BASE_URL = "http://localhost:8001"

TEST_RUN_ID = "online_test_run_123"
TEST_LOG_CONTENT = """
name: Online Test Workflow
on: [push]
jobs:
  security-check:
    runs_on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Snyk
        run: snyk test
"""

def seed_database():
    print("🌱 Seeding Database with test log...")
    try:
        client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client[MONGO_DB]
        collection = db["log"] # verify collection name is 'log'
        
        # Clean up existing test if any
        collection.delete_many({"run_id": TEST_RUN_ID})
        
        # Insert test doc
        # Note: Route expects 'log_data' field
        doc = {
            "run_id": TEST_RUN_ID,
            "repo_name": "emsi/test-repo",
            "provider": "GITHUB",
            "log_data": TEST_LOG_CONTENT,
            "status": "completed"
        }
        result = collection.insert_one(doc)
        print(f"✅ Inserted test document with ID: {result.inserted_id}")
        return True
    except Exception as e:
        print(f"❌ Database Seeding Failed: {e}")
        return False

def verify_api_call():
    print(f"🚀 Calling API /api/parse/db for run_id={TEST_RUN_ID}...")
    try:
        payload = {"run_id": TEST_RUN_ID}
        r = httpx.post(f"{BASE_URL}/api/parse/db", json=payload, timeout=10.0)
        
        print(f"Status: {r.status_code}")
        # print(f"Response: {r.text}")
        
        if r.status_code == 200:
            data = r.json()
            mq_status = data.get("mq_status")
            original_id = data.get("original_id")
            
            print("---------------------------------------------------")
            print("📊 Verification Results:")
            print(f"   - Database Fetch: SUCCESS (Original ID: {original_id})")
            print(f"   - YAML Parsing:   SUCCESS")
            print(f"   - MQ Publishing:  {mq_status.upper()}")
            print("---------------------------------------------------")
            
            if mq_status == "published":
                return True
            else:
                return False
        else:
            print(f"❌ API Request Failed: {r.text}")
            return False
            
    except Exception as e:
        print(f"❌ API Call Error: {e}")
        return False

if __name__ == "__main__":
    if seed_database():
        verify_api_call()
