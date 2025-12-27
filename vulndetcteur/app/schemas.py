from typing import List, Optional
from pydantic import BaseModel

class Event(BaseModel):
    event_id: str
    type: str
    job_name: Optional[str] = None
    step_name: Optional[str] = None
    status: Optional[str] = None
    timestamp: Optional[str] = None
    message: str
    scanner: Optional[str] = None
    severity: Optional[str] = None

class Metadata(BaseModel):
    repo: Optional[str] = None
    branch: Optional[str] = None
    pipeline_name: Optional[str] = None
    environment: Optional[str] = None
    duration_seconds: Optional[float] = None

class DetectRequest(BaseModel):
    run_id: str
    provider: str
    metadata: Optional[Metadata] = None
    events: List[Event]

class Location(BaseModel):
    job_name: Optional[str] = None
    step_name: Optional[str] = None
    event_id: Optional[str] = None
    line_excerpt: Optional[str] = None

class Evidence(BaseModel):
    rule: Optional[str] = None
    confidence: Optional[float] = None
    model: Optional[str] = None
    score: Optional[float] = None

class Vulnerability(BaseModel):
    vuln_id: str
    owasp_category: str
    severity: str
    description: str
    location: Location
    evidence: Evidence
    suggested_fix_key: Optional[str] = None

class DetectResponse(BaseModel):
    run_id: str
    risk_score: float
    vulnerabilities: List[Vulnerability]
