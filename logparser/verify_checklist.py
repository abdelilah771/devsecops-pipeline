
import asyncio
import httpx
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
BASE_URL = "http://127.0.0.1:8001"

async def test_health():
    print("--- 1. Testing /health ---")
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{BASE_URL}/health")
            print(f"Status: {resp.status_code}")
            print(f"Body: {resp.json()}")
            assert resp.status_code == 200
            assert resp.json()["status"] == "healthy"
            print("✅ /health passed")
        except Exception as e:
            print(f"❌ /health failed: {e}")

async def test_parsing_flow():
    print("\n--- 2. Testing /parse (Data Flow) ---")
    
    # 1. Setup Mock Data in MongoDB
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    logs_col = db["Log"]
    events_col = db["ParsedEvents"]
    
    test_run_id = "test_run_check_123"
    
    # Clean previous
    logs_col.delete_one({"run_id": test_run_id})
    events_col.delete_many({"run_id": test_run_id})
    
    mock_log = {
        "run_id": test_run_id,
        "provider": "GITHUB",
        "repo_name": "emsi/logparser",
        "pipeline_name": "test-pipeline",
        "timestamp_received": datetime.now(),
        "author": "tester",
        "log_data": """
##[group]Run actions/checkout@v4
Content of checkout...
##[endgroup]
##[group]Run setup-python
Setting up python...
##[endgroup]
        """
    }
    
    logs_col.insert_one(mock_log)
    print(f"Inserted mock log for {test_run_id}")
    
    # 2. Call /parse
    async with httpx.AsyncClient() as client:
        payload = {"run_id": test_run_id, "provider": "GITHUB"}
        try:
            resp = await client.post(f"{BASE_URL}/parse", json=payload, timeout=30.0)
            print(f"Parse Status: {resp.status_code}")
            print(f"Parse Body: {resp.json()}")
            
            assert resp.status_code == 200
            data = resp.json()
            assert data["success"] is True
            assert data["events_parsed"] >= 2
            print("✅ /parse API call passed")
            
        except Exception as e:
            print(f"❌ /parse failed: {e}")
            return

    # 3. Verify ParsedEvents in MongoDB
    count = events_col.count_documents({"run_id": test_run_id})
    print(f"Found {count} events in ParsedEvents collection")
    assert count >= 2
    
    event = events_col.find_one({"run_id": test_run_id})
    print("Sample Event:", event.get("step_name"), event.get("event_type"))
    assert event.get("provider") == "GITHUB"
    print("✅ MongoDB verification passed")

    # 4. Verify RabbitMQ (via Log output for now, manual check possible)
    print("Check terminal logs for '✅ RabbitMQ Publish SUCCESS'")

async def test_validation():
    print("\n--- 3. Testing Validation ---")
    async with httpx.AsyncClient() as client:
        # Invalid run_id
        payload = {"run_id": "invalid-run-id!", "provider": "GITHUB"}
        resp = await client.post(f"{BASE_URL}/parse", json=payload)
        print(f"Invalid run_id Status: {resp.status_code}")
        if resp.status_code == 422:
            print("✅ Validation caught invalid run_id")
        else:
            print(f"❌ Validation FAILED. Status: {resp.status_code}")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(test_health())
    loop.run_until_complete(test_parsing_flow())
    loop.run_until_complete(test_validation())
