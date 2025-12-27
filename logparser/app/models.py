from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
import re

class ParseRequest(BaseModel):
    run_id: str = Field(default="test_run", max_length=100)
    provider: str = Field(default="GITHUB")
    log_data: Optional[str | dict] = None

    @field_validator('run_id')
    @classmethod
    def validate_run_id(cls, v: str) -> str:
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('run_id must be alphanumeric with underscores only')
        return v

class ParsedEvent(BaseModel):
    run_id: str
    provider: str
    repo_name: Optional[str] = None
    pipeline_name: Optional[str] = None
    job_name: Optional[str] = None
    step_name: Optional[str] = None
    event_type: str  # "step" | "command" | "scanner_alert" | ...
    status: Optional[str] = None
    message: str
    timestamp: Optional[str] = None

class ParseResponse(BaseModel):
    success: bool
    run_id: str
    events_parsed: int
    message: str
