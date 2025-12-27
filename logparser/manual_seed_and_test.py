import pymongo
import os
import httpx
from dotenv import load_dotenv

# Run this script to MANUALLY insert the log your Simulator is missing
# This proves the parser works if the data exists.

load_dotenv()
URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB")
RUN_ID = "SIM_GITHUB_1766851948144"  # The ID you are trying to parse

def manual_seed():
    print(f"🔧 Manually seeding DB for Run ID: {RUN_ID}")
    client = pymongo.MongoClient(URI, serverSelectionTimeoutMS=5000)
    db = client[DB_NAME]
    coll = db["log"]
    
    # Check if exists
    if coll.find_one({"run_id": RUN_ID}):
        print("⚠️ Log already exists. proceeding to parse call...")
    else:
        doc = {
            "run_id": RUN_ID,
            "repo_name": "emsi/manual-seed-repo",
            "provider": "GITHUB",
            "log_data": "name: Manual Seed Workflow\non: [push]\njobs:\n  test:\n    runs_on: ubuntu-latest\n    steps:\n      - run: echo 'seeded'",
            "status": "completed"
        }
        coll.insert_one(doc)
        print("✅ Log inserted successfully!")

    # Now call the API
    url = "http://localhost:8001/api/parse/db"
    print(f"🚀 Calling API: {url}")
    try:
        resp = httpx.post(url, json={"run_id": RUN_ID}, timeout=10.0)
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    manual_seed()
