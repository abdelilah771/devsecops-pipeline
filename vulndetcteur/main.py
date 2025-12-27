from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from typing import List
import threading
import uuid
import logging

from schemas import DetectRequest, DetectResponse, Vulnerability, Event
from app.database import engine, Base, get_db, get_mongo_db
from app.models import VulnerabilityModel
from app.detection import run_detection_logic
from app.crud import insert_vulnerabilities
from app.consumer import start_consumer

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="VulnDetector",
    description="CI/CD Vulnerability Detection microservice (SafeOps-LogMiner)",
    version="1.0.0"
)

logger = logging.getLogger(__name__)

@app.on_event("startup")
def startup_event():
    # Start RabbitMQ consumer in a background thread
    consumer_thread = threading.Thread(target=start_consumer, daemon=True)
    consumer_thread.start()
    logger.info("Started RabbitMQ consumer thread")

@app.get("/health")
def health():
    return {"status": "ok", "service": "VulnDetector"}

@app.post("/detect", response_model=DetectResponse)
def detect_vulnerabilities_endpoint(req: DetectRequest):
    """
    Trigger detection manually for a given run_id.
    Fetches events from MongoDB.
    """
    run_id = req.run_id
    
    # 1. Fetch events from MongoDB
    mongo_db = get_mongo_db()
    parsed_events_collection = mongo_db["ParsedEvents"]
    
    # Assuming one document per run or multiple documents with run_id
    logger.info(f"Querying ParsedEvents for run_id={run_id}")
    cursor = parsed_events_collection.find({"run_id": run_id})
    events_list = list(cursor)
    logger.info(f"Found {len(events_list)} events for run_id={run_id}")
    
    pydantic_events = []
    if events_list:
        for doc in events_list:
            doc.pop("_id", None)
            try:
                ev = Event(**doc)
                pydantic_events.append(ev)
            except Exception as e:
                logger.error(f"Error parsing event: {e}")
    else:
        # Fallback: if no events in DB, maybe they are in the request?
        if req.events:
             pydantic_events = req.events
        else:
             logger.warning(f"No events found for run_id {run_id} in DB and none provided in request.")

    # 2. Run logic
    vulns = run_detection_logic(run_id, pydantic_events)
    
    # 3. Store in DB
    db = next(get_db()) # Manually get db session
    try:
        insert_vulnerabilities(db, vulns)
    finally:
        db.close()
    
    # 4. Calculate risk score (simple logic)
    severity_weights = {"LOW": 0.2, "MEDIUM": 0.5, "HIGH": 0.8, "CRITICAL": 1.0}
    if vulns:
        risk_score = max(severity_weights.get(v.severity, 0.5) for v in vulns)
    else:
        risk_score = 0.0

    return DetectResponse(
        run_id=run_id,
        risk_score=risk_score,
        vulnerabilities=vulns
    )
