import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8004" # Using port 8004 to avoid conflict with stale FixSuggester on 8002

def test_health():
    try:
        r = requests.get(f"{BASE_URL}/health")
        if r.status_code == 200:
            logger.info(f"✅ /health check passed: {r.json()}")
        else:
            logger.error(f"❌ /health check failed: {r.status_code}")
    except Exception as e:
        logger.error(f"❌ /health check connection error: {e}")

def test_vulnerabilities():
    endpoint = f"{BASE_URL}/vulnerabilities"
    try:
        r = requests.get(endpoint)
        if r.status_code == 200:
            data = r.json()
            logger.info(f"✅ /vulnerabilities check passed. Count: {len(data)}")
            if data:
                logger.info(f"   Sample: {data[0]['owasp_category']}")
        else:
            logger.error(f"❌ /vulnerabilities check failed: {r.status_code} - {r.text}")
    except Exception as e:
        logger.error(f"❌ /vulnerabilities connection error: {e}")

def test_stats():
    endpoint = f"{BASE_URL}/stats"
    try:
        r = requests.get(endpoint)
        if r.status_code == 200:
            data = r.json()
            logger.info(f"✅ /stats check passed: {json.dumps(data, indent=2)}")
        else:
            logger.error(f"❌ /stats check failed: {r.status_code} - {r.text}")
    except Exception as e:
        logger.error(f"❌ /stats connection error: {e}")

if __name__ == "__main__":
    test_health()
    test_vulnerabilities()
    test_stats()
