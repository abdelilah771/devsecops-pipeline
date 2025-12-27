from sqlalchemy.orm import Session
from schemas import Vulnerability
from .models import VulnerabilityModel
from typing import List

def insert_vulnerabilities(db: Session, vulns: List[Vulnerability]):
    """
    Bulk inserts a list of vulnerabilities into the database.
    """
    if not vulns:
        return

    db_vulns = []
    for v in vulns:
        db_vuln = VulnerabilityModel(
            vuln_id=v.vuln_id,
            run_id=v.run_id,
            owasp_category=v.owasp_category,
            severity=v.severity,
            description=v.description,
            suggested_fix_key=v.suggested_fix_key,
            location=v.location.model_dump(),  # Convert Pydantic model to dict/JSON
            evidence=v.evidence.model_dump()   # Convert Pydantic model to dict/JSON
        )
        db_vulns.append(db_vuln)

    db.add_all(db_vulns)
    db.commit()

def get_vulnerabilities(db: Session, run_id: str = None, limit: int = 100):
    """
    Fetch vulnerabilities with optional filtering.
    """
    query = db.query(VulnerabilityModel)
    if run_id:
        query = query.filter(VulnerabilityModel.run_id == run_id)
    return query.limit(limit).all()

def get_vulnerability_stats(db: Session):
    """
    Get aggregated statistics for the dashboard.
    """
    total = db.query(VulnerabilityModel).count()
    
    # Severity counts
    severity_counts = {}
    for sev in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]:
        count = db.query(VulnerabilityModel).filter(VulnerabilityModel.severity == sev).count()
        severity_counts[sev] = count
        
    return {
        "total_vulnerabilities": total,
        "severity_counts": severity_counts,
        # You could add recent_detects, top_categories etc here
    }

