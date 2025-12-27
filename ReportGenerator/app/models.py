from sqlalchemy import Column, Integer, String, DateTime, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os

Base = declarative_base()

# SQLAlchemy Model for Reports Table
class Report(Base):
    __tablename__ = "reports"

    report_id = Column(String, primary_key=True, index=True)
    run_id = Column(String, index=True)
    report_type = Column(String)  # executive, technical, compliance
    format = Column(String)       # pdf, html, json
    file_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    expiration_date = Column(DateTime)

class FixProposal(Base):
    __tablename__ = "fix_proposals"

    id = Column(Integer, primary_key=True, index=True)
    vuln_id = Column(String)
    fix = Column(String)
    explanation = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Helper properties for compatibility
    @property
    def proposed_fix(self): return self.fix

    # Check if other columns exist or if I should remove them?
    # Based on output: id, scan_id, vuln_id, fix, timestamp.
    # The others: file_path, line_number, original_code, confidence_score, severity, model_name, status seem missing.
    # I should remove them to avoid UndefinedColumn error.
    
    # Mapping for convenience in code (optional helper property)
    @property
    def run_id(self): return self.scan_id
    @property
    def proposed_fix(self): return self.fix

# Pydantic Models for Request/Response
class Vulnerability(BaseModel):
    id: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    category: str  # OWASP category
    description: str
    affected_component: str
    line_number: Optional[int] = None
    fix_suggestion: Optional[str] = None
    cve_id: Optional[str] = None

class ScanMetrics(BaseModel):
    total_vulnerabilities: int = 0
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    security_score: float = 0.0

class ReportRequest(BaseModel):
    run_id: str
    report_type: str = "technical"  # executive, technical, compliance
    format: str = "pdf"             # pdf, html, json
    vulnerabilities: List[Vulnerability] = []
    metrics: ScanMetrics = ScanMetrics()
    project_name: str = "Unknown Project"
    triggered_by: str = "CI/CD"

class ReportResponse(BaseModel):
    task_id: str
    status: str
