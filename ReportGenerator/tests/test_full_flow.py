import os
import time
import sys

# Ensure we use SQLite for both API and Worker (shared file)
# We MUST set this before importing app
os.environ["DATABASE_URL"] = "sqlite:///./test_reports.db"

# Ensure Eager mode is OFF to use real Redis
os.environ["CELERY_ALWAYS_EAGER"] = "false"

# Set Matplotlib to Headless
os.environ["MPLBACKEND"] = "Agg"

from fastapi.testclient import TestClient
from app.main import app

# Initialize TestClient
client = TestClient(app)

def run_integration_test():
    print("🚀 Starting Integration Test (Redis + Celery Worker)")
    
    # 1. Prepare Payload
    payload = {
        "run_id": "REDIS-RUN-001",
        "report_type": "executive",
        "format": "html",
        "project_name": "Redis Integrated Project",
        "metrics": {
            "total_vulnerabilities": 8,
            "critical_count": 1,
            "high_count": 2,
            "medium_count": 3,
            "low_count": 2,
            "security_score": 72.0
        },
        "vulnerabilities": [
            {"id": "V1", "severity": "CRITICAL", "category": "Injection", "description": "SQLi", "affected_component": "Login"},
            {"id": "V2", "severity": "HIGH", "category": "XSS", "description": "Reflected XSS", "affected_component": "Search"}
        ]
    }

    # 2. Call API
    print("📡 Sending Request...")
    response = client.post("/generate", json=payload)
    if response.status_code != 202:
        print(f"❌ Failed: {response.text}")
        return
    
    task_id = response.json()["task_id"]
    print(f"✅ Task Submitted. ID: {task_id}")

    # 3. Poll Status
    print("⏳ Waiting for Celery Worker...")
    for i in range(20):
        res = client.get(f"/status/{task_id}")
        data = res.json()
        status = data["status"]
        print(f"   [{i}s] Status: {status}")
        
        if status == "SUCCESS":
            file_url = data["result"]["file_url"]
            print(f"🎉 SUCCESS! Report: {file_url}")
            # Save file path to a temp file so the agent can read it later if needed
            with open("last_report_path.txt", "w") as f:
                f.write(file_url)
            return
        elif status == "FAILURE":
            print(f"❌ Task Failed! {data}")
            return
        
        time.sleep(1)

    print("❌ Timeout waiting for worker.")

if __name__ == "__main__":
    run_integration_test()
