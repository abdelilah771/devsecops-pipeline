from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.models import ReportRequest, ReportResponse, Base, Report
from app.database import engine, get_db
from app.tasks.celery_tasks import generate_report_task, celery_app
from celery.result import AsyncResult
import uvicorn

# Create DB Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ReportGenerator Microservice", version="1.0.0")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate", response_model=ReportResponse, status_code=202)
def generate_report(request: ReportRequest):
    """
    Endpoint to trigger report generation.
    Returns a task_id to track progress.
    """
    # Trigger Celery Task
    # We pass the pydantic model as a dict so it can be serialized
    task = generate_report_task.delay(request.model_dump())
    
    return ReportResponse(task_id=task.id, status="PROCESSING")

@app.get("/status/{task_id}")
def get_status(task_id: str):
    """
    Check the status of a generation task.
    """
    task_result = AsyncResult(task_id, app=celery_app)
    result = {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result
    }
    return result

@app.get("/download/{report_id}")
def download_report(report_id: str, db: Session = Depends(get_db)):
    """
    Get the download URL for a generated report.
    """
    report = db.query(Report).filter(Report.report_id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return {"file_url": report.file_url}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8005))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
