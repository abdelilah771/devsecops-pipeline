import httpx
import json

BASE_URL = "http://localhost:8001"

def test_health():
    print("Testing /health...")
    try:
        r = httpx.get(f"{BASE_URL}/health", timeout=5.0)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.json()}")
        if r.status_code == 200:
            print("✅ Health check PASSED (Offline Mode)")
        else:
            print("❌ Health check FAILED")
    except Exception as e:
        print(f"❌ Health check ERROR: {e}")

def test_parse():
    print("\nTesting /parse (Offline)...")
    payload = {
        "log_data": "name: test-log\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n    - name: Checkout\n      uses: actions/checkout@v2",
        "provider": "GITHUB"
    }
    try:
        r = httpx.post(f"{BASE_URL}/api/parse", json={"yaml": payload["log_data"]}, timeout=10.0)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text}")
        if r.status_code == 200:
            data = r.json()
            if data.get("mq_status") == "published":
                print("✅ Parse test PASSED & Published to MQ")
            else:
                print("⚠️ Parse test PASSED but MQ Publish FAILED")
        else:
            print("❌ Parse test FAILED")
    except Exception as e:
        print(f"❌ Parse test ERROR: {e}")

if __name__ == "__main__":
    test_health()
    test_parse()
