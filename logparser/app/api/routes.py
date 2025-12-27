from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from app.parser.yaml_parser import parse_workflow
from app.parser.feature_extractor import extract_security_features

router = APIRouter()

class ParseRequest(BaseModel):
    yaml: str

from app.messaging.publisher import publish_parsed_event

@router.post("/api/parse")
async def parse_yaml(request: ParseRequest):
    """Endpoint test pour parser YAML manuellement"""
    try:
        parsed = parse_workflow(request.yaml)
        features = extract_security_features(parsed)
        
        # Publish to RabbitMQ (Integration with VulnDetector)
        mq_success = publish_parsed_event({
            "parsed_workflow": parsed,
            "features": features,
            "repository": "manual-test", 
            "original_id": "manual"
        })
        
        return {
            "parsed": parsed,
            "features": features,
            "mq_status": "published" if mq_success else "failed"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

from app.models.schemas import DBParseRequest
from app.database.mongodb import mongodb
from app.config.settings import settings

@router.post("/api/parse/db")
async def parse_from_db(request: DBParseRequest):
    """
    Récupère un log depuis la collection 'log' de MongoDB et le parse.
    """
    if not mongodb.is_connected:
         raise HTTPException(status_code=503, detail="Database disconnected")
         
    collection = mongodb.get_collection("log") # Collection name 'log' without s
    
    # Query by run_id
    log_entry = collection.find_one({"run_id": request.run_id})
    
    if not log_entry:
        raise HTTPException(status_code=404, detail=f"Log not found for run_id: {request.run_id}")
        
    raw_content = log_entry.get("log_data", "")
    if not raw_content:
         raise HTTPException(status_code=400, detail="Log entry has no data")
         
    try:
        parsed = parse_workflow(raw_content)
        features = extract_security_features(parsed)
        
        # Publish to RabbitMQ (Integration with VulnDetector)
        mq_success = publish_parsed_event({
            "parsed_workflow": parsed,
            "features": features,
            "repository": log_entry.get("repo_name", "unknown"),
             "original_id": str(log_entry.get("_id"))
        })
        
        return {
            "parsed": parsed,
            "features": features,
            "original_id": str(log_entry.get("_id")),
            "mq_status": "published" if mq_success else "failed"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing error: {str(e)}")

from app.models.schemas import LogEntryResponse

@router.get("/logs", response_model=List[LogEntryResponse])
async def get_logs(
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    provider: Optional[str] = None
):
    """
    Retrieve raw logs from the database with pagination and filtering.
    """
    if not mongodb.is_connected:
        raise HTTPException(status_code=503, detail="Database disconnected")
        
    collection = mongodb.get_collection("log")
    
    # Build Query
    filter_query = {}
    if provider:
        filter_query["provider"] = provider
        
    try:
        cursor = collection.find(filter_query).sort("_id", -1).skip(skip).limit(limit)
        logs = list(cursor)
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Retrieval Error: {str(e)}")
