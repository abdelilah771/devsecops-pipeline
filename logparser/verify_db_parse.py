import httpx
import json

BASE_URL = "http://localhost:8001"

def test_db_parse():
    print("Testing /api/parse/db...")
    # Using a run_id that hopefully exists or at least tests the DB connection flow
    payload = {
        "run_id": "test_run_1", 
        "provider": "GITHUB"
    }
    
    try:
        r = httpx.post(f"{BASE_URL}/api/parse/db", json=payload, timeout=5.0)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text}")
        
        if r.status_code in [200, 404]: 
            # 404 is acceptable if DB is empty, as it proves we successfully queried the DB
            print("✅ DB Parse Endpoint Reachable")
        elif r.status_code == 503:
            print("❌ DB Disconnected (Expected if DNS still down)")
        else:
            print(f"❌ Unexpected Status: {r.status_code}")
            
    except Exception as e:
        print(f"❌ Request Error: {e}")

if __name__ == "__main__":
    test_db_parse()
