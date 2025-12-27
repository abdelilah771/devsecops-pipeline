import pymongo
import httpx
import os
import uuid
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Configuration ---
MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGODB_DB", "safeops-logminer")
LOGPARSER_URL = "http://localhost:8001/api/parse/db"

def simulate_log_flow():
    # 1. Generate Fake Data
    run_id = f"SIM_{uuid.uuid4().hex[:8]}"
    print(f"🔄 [Step 1] Generated content for Run ID: {run_id}")
    
    log_content = f"""
    name: Simulation Run {run_id}
    on: [push]
    jobs:
      security-check:
        runs_on: ubuntu-latest
        steps:
          - uses: actions/checkout@v2
          - name: Run Snyk
            run: snyk test --severity-threshold=high
    """
    
    doc = {
        "run_id": run_id,
        "repo_name": "simulation/test-repo",
        "provider": "GITHUB",
        "log_data": log_content,
        "status": "completed",
        "timestamp": datetime.now()
    }

    # 2. SAVE to MongoDB (CRITICAL STEP)
    # The LogParser API expects the data to be in the DB *before* you call it.
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        collection = db["log"]
        collection.insert_one(doc)
        print("💾 [Step 2] Saved log to MongoDB.")
    except Exception as e:
        print(f"❌ [Step 2] DB Save Failed: {e}")
        return

    # 3. CALL LogParser API
    # Now we tell the parser: "Hey, data for run_id X is ready in the DB, go process it."
    print(f"🚀 [Step 3] Triggering LogParser API for {run_id}...")
    try:
        payload = {"run_id": run_id, "provider": "GITHUB"}
        response = httpx.post(LOGPARSER_URL, json=payload, timeout=10.0)
        
        if response.status_code == 200:
            print("✅ [Success] Parser Status:", response.status_code)
            print("   MQ Status:", response.json().get('mq_status'))
        else:
            print(f"⚠️ [Failure] Status: {response.status_code}")
            print("   Detail:", response.text)
            
    except Exception as e:
        print(f"❌ [Step 3] API Call Failed: {e}")

if __name__ == "__main__":
    simulate_log_flow()
