import httpx

BASE_URL = "http://localhost:8001"

def test_incorrect_call():
    print("\n🔴 Testing Incorrect Call (What you are doing):")
    print("Request: POST /api/parse?run_id=TEST_ID")
    try:
        # Mimicking the user's log: POST /api/parse?run_id=...
        r = httpx.post(f"{BASE_URL}/api/parse", params={"run_id": "TEST_ID"}, json={}) 
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text}")
    except Exception as e:
        print(f"Error: {e}")

def test_correct_call():
    print("\n🟢 Testing Correct Call (What you need to do):")
    print("Request: POST /api/parse/db")
    print("Body: {'run_id': 'TEST_ID'}")
    try:
        # Correct usage
        r = httpx.post(f"{BASE_URL}/api/parse/db", json={"run_id": "TEST_ID"})
        print(f"Status: {r.status_code}")
        # 404 is okay (Log not found), it means the Request Format was valid!
        # 422 means Request Format was INVALID.
        if r.status_code == 422:
             print("Response: 422 UNPROCESSABLE (Failed)")
        else:
             print(f"Response: {r.status_code} (Success / Valid Format)")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_incorrect_call()
    test_correct_call()
