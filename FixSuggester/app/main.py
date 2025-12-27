from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": settings.PROJECT_NAME}

@app.get("/")
def root():
    return {"message": "Welcome to FixSuggester Service"}

from app.services.fix_generator import FixGenerator

@app.post("/fix/{vuln_id}")
async def create_fix(vuln_id: str):
    generator = FixGenerator()
    result = await generator.generate_fix(vuln_id)
    return result

from app.services.postgres_service import PostgresService

@app.get("/fixes/{vuln_id}")
async def get_fix(vuln_id: str):
    pg_service = PostgresService()
    fix = await pg_service.get_fix_proposal(vuln_id)
    if not fix:
        return {"error": "Fix not found"}
    return fix
