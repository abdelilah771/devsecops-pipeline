
import asyncio
import httpx
from datetime import datetime
from pymongo import MongoClient
from app.config import settings

# Test Data
RUN_ID = "test_auto_run_001"
PROVIDER = "GITHUB"
REPO_NAME = "demo/repo"

LOG_CONTENT = """##[group]Run actions/checkout@v2
...
### Checkout
...
Completed with exit code 0
"""

def seed_db():
    print(f"Seeding DB with run_id={RUN_ID}...")
    client = MongoClient(settings.mongo_uri)
    db = client[settings.mongo_db]
    logs_col = db["Log"]
    
    # Clean up existing if any
    logs_col.delete_many({"run_id": RUN_ID})
    
    # Insert Log
    log_doc = {
        "run_id": RUN_ID,
        "provider": PROVIDER,
        "repo_name": REPO_NAME,
        "log_data": LOG_CONTENT,
        "timestamp_received": datetime.utcnow(),
        "pipeline_name": "test-pipeline",
        "author": "tester",
        "timestamp_original": datetime.utcnow()
    }
    logs_col.insert_one(log_doc)
    print("Log inserted.")

async def trigger_parse():
    print("Triggering /parse endpoint...")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8001/parse",
            json={"run_id": RUN_ID, "provider": PROVIDER}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")

if __name__ == "__main__":
    seed_db()
    asyncio.run(trigger_parse())
