import httpx

BASE_URL = "http://localhost:8001"

def verify_get_logs():
    print(f"🚀 Testing GET {BASE_URL}/logs ...")
    try:
        # Default call
        r = httpx.get(f"{BASE_URL}/logs", timeout=10.0)
        
        if r.status_code == 200:
            logs = r.json()
            print(f"✅ Success! Retrieved {len(logs)} logs.")
            
            if len(logs) > 0:
                first_log = logs[0]
                print("First Log Entry Preview:")
                print(f" - ID: {first_log.get('_id')}")
                print(f" - Provider: {first_log.get('provider')}")
                print(f" - Repo: {first_log.get('repo_name')}")
                print(f" - RunID: {first_log.get('run_id')}")
                # Verify structure matches expectation
                if 'timestamp_received' in first_log:
                     print(f" - Timestamp: {first_log.get('timestamp_received')}")
                else:
                     print(" ⚠️ Warning: timestamp_received missing (might be optional/null in DB)")
        else:
            print(f"❌ Failed. Status: {r.status_code}")
            print(f"Response: {r.text}")

        # Test filtering
        print("\n🚀 Testing Filtering (provider=GITHUB)...")
        r_filter = httpx.get(f"{BASE_URL}/logs?provider=GITHUB&limit=1", timeout=10.0)
        if r_filter.status_code == 200:
             print(f"✅ Filter Success. Count: {len(r_filter.json())}")
        else:
             print(f"❌ Filter Failed: {r_filter.status_code}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verify_get_logs()
