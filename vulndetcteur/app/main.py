from fastapi import FastAPI, Depends
from typing import List
import uuid
from sqlalchemy.orm import Session

from .schemas import DetectRequest, DetectResponse, Vulnerability, Location, Evidence
from . import models, database, crud

# Create tables on startup
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="VulnDetector",
    description="CI/CD Vulnerability Detection microservice (SafeOps-LogMiner)",
    version="1.0.0"
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "service": "VulnDetector"}

@app.get("/vulnerabilities")
def get_vulnerabilities(run_id: str = None, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_vulnerabilities(db, run_id=run_id, limit=limit)

@app.get("/stats")
def get_stats(db: Session = Depends(database.get_db)):
    return crud.get_vulnerability_stats(db)

@app.on_event("startup")
def startup_event():
    from .ai_engine import ai_engine
    ai_engine.load_models()

@app.post("/detect", response_model=DetectResponse)
def detect_vulnerabilities(req: DetectRequest, db: Session = Depends(database.get_db)):
    vulns: List[Vulnerability] = []

    # 1) Rule: Unpinned Action (GitHub Actions)
    for ev in req.events:
        if "uses:" in ev.message and "@latest" in ev.message:
            vulns.append(
                Vulnerability(
                    vuln_id=str(uuid.uuid4())[:8],
                    owasp_category="CICD-SEC-07: Insecure System Configuration (Unpinned Action)",
                    severity="HIGH",
                    description="GitHub Action is used with mutable tag 'latest' instead of a pinned commit SHA.",
                    location=Location(
                        job_name=ev.job_name,
                        step_name=ev.step_name,
                        event_id=ev.event_id,
                        line_excerpt=ev.message
                    ),
                    evidence=Evidence(
                        rule="unpinned_action_rule",
                        confidence=0.99
                    ),
                    suggested_fix_key="pin_github_action"
                )
            )

    # 2) Rule: Secret Leak
    for ev in req.events:
        lower = ev.message.lower()
        if "secret" in lower or "aws_access_key_id" in lower:
            vulns.append(
                Vulnerability(
                    vuln_id=str(uuid.uuid4())[:8],
                    owasp_category="CICD-SEC-06: Insufficient Credential Hygiene",
                    severity="CRITICAL",
                    description="Possible secret leakage detected in pipeline logs.",
                    location=Location(
                        job_name=ev.job_name,
                        step_name=ev.step_name,
                        event_id=ev.event_id,
                        line_excerpt=ev.message
                    ),
                    evidence=Evidence(
                        rule="secret_leak_rule",
                        confidence=0.95
                    ),
                    suggested_fix_key="mask_secret_in_logs"
                )
            )

    # Save to Database (Basic implementation)
    # This loop demonstrates saving detected vulns to the DB
    for v in vulns:
        db_vuln = models.VulnerabilityModel(
            vuln_id=v.vuln_id,
            owasp_category=v.owasp_category,
            severity=v.severity,
            description=v.description,
            suggested_fix_key=v.suggested_fix_key,
            location=v.location.dict(exclude_none=True),
            evidence=v.evidence.dict(exclude_none=True),
            run_id=req.run_id
        )
        db.add(db_vuln)
    
    if vulns:
        db.commit()

    # Simple risk score calculation
    severity_weights = {"LOW": 0.2, "MEDIUM": 0.5, "HIGH": 0.8, "CRITICAL": 1.0}
    if vulns:
        risk_score = max(severity_weights.get(v.severity, 0.5) for v in vulns)
    else:
        risk_score = 0.0

    return DetectResponse(
        run_id=req.run_id,
        risk_score=risk_score,
        vulnerabilities=vulns
    )

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8004))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
