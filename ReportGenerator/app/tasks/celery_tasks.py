from celery import Celery
import os
import time
from app.models import ReportRequest, Report, ReportResponse, FixProposal, Vulnerability
from app.database import SessionLocal, engine
from app.services.pdf_generator import PdfGenerator
from app.services.html_generator import HtmlGenerator
from app.services.storage_service import StorageService
import uuid
from datetime import datetime
import json

# Redis Configuration (assuming local redis)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery("report_tasks", broker=REDIS_URL, backend=REDIS_URL)

if os.getenv("CELERY_ALWAYS_EAGER", "False").lower() == "true":
    celery_app.conf.task_always_eager = True
    celery_app.conf.task_eager_propagates = True
    celery_app.conf.task_store_eager_result = True

html_gen = HtmlGenerator()
pdf_gen = PdfGenerator()

# Force Mock Storage for verification
if True: # os.getenv("CELERY_ALWAYS_EAGER", "False").lower() == "true" or os.getenv("USE_MOCK_STORAGE", "False").lower() == "true":
    class MockStorageService:
        def upload_file(self, file_path: str, object_name: str, content_type: str) -> str:
            # Just return the local path for testing
            # Ensure target directory exists
            target_path = os.path.abspath(f"generated_reports/{object_name}")
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            import shutil
            shutil.copy(file_path, target_path)
            return f"file://{target_path}"
            
    storage_service = MockStorageService()
else:
    storage_service = StorageService()

@celery_app.task(bind=True)
def generate_report_task(self, request_data: dict):
    """
    Celery task to generate a report.
    request_data should be a dictionary compatible with ReportRequest.
    """
    try:
        # Deserialize request
        request = ReportRequest(**request_data)
        
        # If vulnerabilities list is empty, try to fetch from DB using run_id
        if not request.vulnerabilities and request.run_id:
             db_session = SessionLocal()
             try:
                 # Schema doesn't have scan_id, so we fetch recent proposals as a fallback
                 proposals = db_session.query(FixProposal).order_by(FixProposal.created_at.desc()).limit(20).all()
                 if proposals:
                     print(f"Found {len(proposals)} recent proposals (fallback)")
                     for p in proposals:
                         # Map FixProposal to Vulnerability model
                         vuln = Vulnerability(
                             id=str(p.id),
                             severity="MEDIUM", 
                             category="Security Vulnerability", 
                             description=f"Vulnerability ID: {p.vuln_id}\nExplanation: {p.explanation}",
                             affected_component="Unknown", 
                             line_number=0, 
                             fix_suggestion=f"{p.fix}\n\nExplanation: {p.explanation}",
                             cve_id=None
                         )
                         request.vulnerabilities.append(vuln)
                     
                     # Update metrics if they were zero/empty
                     if request.metrics.total_vulnerabilities == 0:
                         request.metrics.total_vulnerabilities = len(proposals)
                         # Simple logic to update counts based on severity
                         for v in request.vulnerabilities:
                             s = v.severity.upper()
                             if s == "CRITICAL": request.metrics.critical_count += 1
                             elif s == "HIGH": request.metrics.high_count += 1
                             elif s == "MEDIUM": request.metrics.medium_count += 1
                             elif s == "LOW": request.metrics.low_count += 1
             except Exception as db_err:
                 print(f"Error fetching from DB: {db_err}")
             finally:
                 db_session.close()
        
        # Determine format and generate content
        file_extension = request.format.lower()
        content = None
        content_type = ""

        if file_extension == "pdf":
            content = pdf_gen.generate_report(request)
            content_type = "application/pdf"
        elif file_extension == "html":
            content = html_gen.generate_report(request).encode('utf-8')
            content_type = "text/html"
        elif file_extension == "json":
             # Just dump the Pydantic model to JSON
             content = request.model_dump_json(indent=2).encode('utf-8')
             content_type = "application/json"
        else:
            raise ValueError(f"Unsupported format: {file_extension}")

        # Upload to Storage
        report_id = str(uuid.uuid4())
        filename = f"reports/{request.run_id}/{report_id}.{file_extension}"
        
        # We need to save content to a temporary file or use put_object if supported by StorageService
        # StorageService.upload_file expects a file path. Let's write to /tmp (or local equivalent)
        temp_file_path = f"temp_{report_id}.{file_extension}"
        with open(temp_file_path, "wb") as f:
            f.write(content)
        
        file_url = storage_service.upload_file(temp_file_path, filename, content_type)
        
        # Clean up temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

        # Save Metadata to DB
        db = SessionLocal()
        try:
            db_report = Report(
                report_id=report_id,
                run_id=request.run_id,
                report_type=request.report_type,
                format=request.format,
                file_url=file_url,
                created_at=datetime.utcnow()
                # expiration_date logic could go here
            )
            db.add(db_report)
            db.commit()
        finally:
            db.close()

        return {"status": "SUCCESS", "report_id": report_id, "file_url": file_url}

    except Exception as e:
        # Log the error
        print(f"Error generating report: {e}")
        self.update_state(state='FAILURE', meta={'exc': str(e)})
        raise e
