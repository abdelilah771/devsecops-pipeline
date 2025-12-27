from typing import List
import uuid
from schemas import Event, Vulnerability, Location, Evidence

def run_detection_logic(run_id: str, events: List[Event]) -> List[Vulnerability]:
    """
    Analyzes a list of events for a specific run_id and returns detected vulnerabilities.
    """
    vulns: List[Vulnerability] = []

    # 1) Rule: Unpinned Action (GitHub Actions)
    # Checks for 'uses:' directives that use '@latest' or similar mutable tags instead of SHA.
    for ev in events:
        if "uses:" in ev.message and "@latest" in ev.message:
            vulns.append(
                Vulnerability(
                    vuln_id=str(uuid.uuid4())[:8],
                    run_id=run_id,
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
    # Checks for common secret patterns in log messages.
    for ev in events:
        lower_msg = ev.message.lower()
        
        # --- AI ENGINE INTEGRATION ---
        # 1. Extract Features
        # Assuming provider and duration might come from run metadata or default
        # For this function, we don't have metadata passed in easily, so we use defaults or extend helper
        # simplified for now:
        from .ai_engine import ai_engine
        
        features = ai_engine.extract_features(ev.message, provider="unknown", duration_seconds=1.0)
        
        # 2. Predict Risk (Phase 1)
        is_risky, ai_risk_score = ai_engine.predict_risk(features)
        
        if is_risky:
            # 3. Predict Category (Phase 2)
            category, confidence = ai_engine.predict_category(features)
            
            vulns.append(
                Vulnerability(
                    vuln_id=str(uuid.uuid4())[:8],
                    run_id=run_id,
                    owasp_category=category,
                    severity="HIGH" if ai_risk_score > 0.8 else "MEDIUM",
                    description=f"AI-Detected Anomaly: {category} (Confidence: {confidence:.2f})",
                    location=Location(
                        job_name=ev.job_name,
                        step_name=ev.step_name,
                        event_id=ev.event_id,
                        line_excerpt=ev.message[:200]
                    ),
                    evidence=Evidence(
                        rule="ai_model_phase1_phase2",
                        confidence=confidence,
                        model="SafeOps-LogMiner AI",
                        score=ai_risk_score
                    ),
                    suggested_fix_key="review_ai_alert"
                )
            )

        # Basic heuristic for demonstration; in prod, use regex or entropy checks.
        if "secret" in lower_msg or "aws_access_key_id" in lower_msg:
             # Exclude false positives if necessary (e.g., "secret" in a legitimate context)
            vulns.append(
                Vulnerability(
                    vuln_id=str(uuid.uuid4())[:8],
                    run_id=run_id,
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

    return vulns
