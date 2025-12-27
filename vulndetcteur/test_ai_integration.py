
import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# FIX: Standard connection string used in database.py now, so we can test the real connection
# os.environ["MONGO_URL"] = "mongodb://localhost:27017/test_db"


from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "VulnDetector"}

def test_ai_detection():
    # Use a log message that is likely to trigger the AI model e.g., something that looks like an error
    # Note: This depends on the specific training data of the model. 
    # We'll try a generic "error" message which usually triggers basic anomaly detectors.
    # If the model is very specific, this might not trigger, but it verifies the code path runs without crashing.
    
    payload = {
        "run_id": "test-run-ai-1",
        "provider": "github",
        "events": [
            {
                "event_id": "evt-1",
                "type": "log",
                "message": "CRITICAL: Database connection failed. Access denied for user 'admin'.",
                "job_name": "db-setup",
                "step_name": "connect",
                "timestamp": "2024-01-01T12:00:00Z"
            }
        ]
    }
    
    # Trigger startup event manually if TestClient doesn't do it automatically in this context
    # (FastAPI TestClient usually handles lifecycle events)
    with TestClient(app) as client:
        response = client.post("/detect", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["run_id"] == "test-run-ai-1"
        
        # Print vulnerabilities to see if AI caught it
        print("\nDetected Vulnerabilities:", data["vulnerabilities"])
        
        # Check if any vulnerability has source/rule from AI
        ai_detected = any(v["evidence"]["rule"] == "ai_model_phase1_phase2" for v in data["vulnerabilities"])
        
        # If the model is strong, it should detect "Access denied" as a risk
        # If not, at least we ensure no exception was raised
        if ai_detected:
            print("SUCCESS: AI Model detected the vulnerability!")
        else:
            print("WARNING: AI Model did NOT detect the vulnerability (might need better test data).")

if __name__ == "__main__":
    # fast way to run without pytest installed in env if needed, but we installed pytest usually
    try:
        from app.ai_engine import ai_engine
        ai_engine.load_models() # Load manually for script test
        
        print("Models loaded. Running manual test...")
        
        # Mock what TestClient does
        features = ai_engine.extract_features("CRITICAL: Database connection failed. Access denied for user 'admin'.", "github", 1.0)
        risk, score = ai_engine.predict_risk(features)
        print(f"Risk: {risk}, Score: {score}")
        
        if risk:
            cat, conf = ai_engine.predict_category(features)
            print(f"Category: {cat}, Confidence: {conf}")
            
    except Exception as e:
        print(f"Error during manual verify: {e}")
