import os
import time
import json

# Enable Eager Mode for Celery (Must be before importing app)
os.environ["CELERY_ALWAYS_EAGER"] = "true"
# Use SQLite for testing to avoid Postgres dependency
os.environ["DATABASE_URL"] = "sqlite:///./test_reports.db"
# Set Matplotlib backend to Agg (Headless)
os.environ["MPLBACKEND"] = "Agg"

from fastapi.testclient import TestClient
from app.main import app
from app.models import ReportRequest, Vulnerability, ScanMetrics

# Initialize TestClient
client = TestClient(app)

def simulate_generate_report():
    print("🚀 Simulating User Action: 'Click Generate Report'")
    
    # 1. Prepare Data
    metrics = {
        "total_vulnerabilities": 12,
        "critical_count": 2,
        "high_count": 5,
        "medium_count": 3,
        "low_count": 2,
        "security_score": 45.5
    }
    
    vulns = [
        {
            "id": "VULN-1", "severity": "CRITICAL", "category": "Injection",
            "description": "SQL Injection found in search field", "affected_component": "SearchService",
            "line_number": 45, "fix_suggestion": "Use parameterized queries"
        },
        {
            "id": "VULN-2", "severity": "HIGH", "category": "XSS",
            "description": "Reflected XSS in login page", "affected_component": "AuthService",
            "line_number": 12, "fix_suggestion": "Sanitize user input"
        },
         {
            "id": "VULN-3", "severity": "MEDIUM", "category": "Misconfiguration",
            "description": "Debug mode enabled", "affected_component": "Config",
            "line_number": 0, "fix_suggestion": "Disable debug mode in prod"
        }
    ]

    payload = {
        "run_id": "SIM-RUN-002",
        "report_type": "executive",
        "format": "html",
        "project_name": "E-Commerce Platform",
        "metrics": metrics,
        "vulnerabilities": vulns
    }

    try:
        # 2. Call API via TestClient
        print(f"📡 Sending POST request to /generate...")
        
        response = client.post("/generate", json=payload)
        
        if response.status_code != 202:
            print(f"❌ Request Failed! Status: {response.status_code}")
            print(response.json())
            return

        data = response.json()
        task_id = data["task_id"]
        print(f"✅ Request Accepted! Task ID: {task_id}")

        # 3. Poll for Status (In Eager mode, it should be done immediately, but we keep logic)
        print("⏳ Polling for completion...")
        for _ in range(5): 
            status_res = client.get(f"/status/{task_id}")
            status_data = status_res.json()
            status = status_data["status"]
            print(f"   Status: {status}")
            
            if status == "SUCCESS":
                result = status_data.get("result", {})
                file_url = result.get("file_url")
                print(f"🎉 Report Generated Successfully!")
                print(f"📂 Download URL: {file_url}")
                
                # Verify file content
                if file_url.startswith("file://"):
                   path = file_url.replace("file://", "")
                   if os.path.exists(path):
                       print(f"   File verified on disk: {path}")
                       print(f"   Size: {os.path.getsize(path)} bytes")
                return
            elif status == "FAILURE":
                print("❌ Generation Failed!")
                print(status_data)
                return
            
            time.sleep(0.5)
        
        print("⚠️ Timeout waiting for report generation.")

    except Exception as e:
        print(f"❌ Error during simulation: {e}")

if __name__ == "__main__":
    simulate_generate_report()
