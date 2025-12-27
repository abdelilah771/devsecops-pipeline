from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field, BeforeValidator
from typing_extensions import Annotated

# Helper for MongoDB ObjectId
PyObjectId = Annotated[str, BeforeValidator(str)]

class WorkflowMessage(BaseModel):
    repository: str
    workflow: Dict
    _id: Optional[str] = None

class DBParseRequest(BaseModel):
    run_id: str
    provider: str = "GITHUB"

class ParsedEvent(BaseModel):
    repository: str
    parsed_workflow: Dict
    features: Dict
    original_id: Optional[str] = None

class LogEntryResponse(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    timestamp_received: Optional[datetime] = None
    provider: str = "GITHUB"
    repo_name: str = "unknown"
    run_id: str
    log_data: str

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}
