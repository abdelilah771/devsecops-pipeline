import asyncpg
from app.core.config import settings

class PostgresService:
    async def get_connection(self):
        if settings.POSTGRES_URI:
            return await asyncpg.connect(settings.POSTGRES_URI)
        return await asyncpg.connect(
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_SERVER,
            database=settings.POSTGRES_DB
        )

    async def ensure_tables_exist(self):
        conn = await self.get_connection()
        try:
            # Create fix_proposals table if it doesn't exist
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS fix_proposals (
                    id SERIAL PRIMARY KEY,
                    vuln_id VARCHAR(255) UNIQUE NOT NULL,
                    fix TEXT NOT NULL,
                    explanation TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            # Ensure vulnerabilities table exists (it should, but just in case for testing)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS vulnerabilities (
                     id VARCHAR(255) PRIMARY KEY,
                     description TEXT,
                     code TEXT,
                     language VARCHAR(50)
                );
            """)
        finally:
            await conn.close()

    async def fetch_unprocessed_vulnerabilities(self):
        conn = await self.get_connection()
        try:
            # Fetch vulnerabilities that do not have a corresponding entry in fix_proposals
            # Extract 'code' from location->>'line_excerpt'
            rows = await conn.fetch("""
                SELECT 
                    v.vuln_id as id, 
                    v.description, 
                    v.location->>'line_excerpt' as code, 
                    'unknown' as language 
                FROM vulnerabilities v
                LEFT JOIN fix_proposals fp ON v.vuln_id = fp.vuln_id
                WHERE fp.id IS NULL
            """)
            return [dict(row) for row in rows]
        finally:
            await conn.close()

    async def get_vulnerability(self, vuln_id: str):
        if settings.MOCK_DB:
            mocks = {
                "vuln-sqli": {
                    "id": "vuln-sqli",
                    "description": "SQL Injection in login form",
                    "code": "query = 'SELECT * FROM users WHERE username = ' + username",
                    "language": "python"
                },
                "vuln-xss": {
                    "id": "vuln-xss",
                    "description": "Reflected XSS in search parameter",
                    "code": "return f'<h1>Search results for: {user_input}</h1>'",
                    "language": "python"
                },
                "vuln-secret": {
                    "id": "vuln-secret",
                    "description": "Hardcoded AWS Access Key",
                    "code": "AWS_KEY = 'AKIA1234567890EXAMPLE'",
                    "language": "python"
                }
            }
            return mocks.get(vuln_id, mocks["vuln-sqli"])
            
        conn = await self.get_connection()
        try:
            # Query placeholder - normalized to return expected keys
            row = await conn.fetchrow("""
                SELECT 
                    vuln_id as id, 
                    description, 
                    location->>'line_excerpt' as code, 
                    'unknown' as language 
                FROM vulnerabilities 
                WHERE vuln_id = $1
            """, vuln_id)
            return dict(row) if row else None
        finally:
            await conn.close()

    async def save_fix_proposal(self, vuln_id: str, fix_data: dict):
        if settings.MOCK_DB:
            print(f"[MOC] Saved fix proposal for {vuln_id}: {fix_data.get('fixed_code')[:20]}...")
            return True

        conn = await self.get_connection()
        try:
            # Upsert logic or simple insert
            await conn.execute(
                """
                INSERT INTO fix_proposals (vuln_id, fix, explanation, created_at)
                VALUES ($1, $2, $3, NOW())
                ON CONFLICT (vuln_id) DO UPDATE 
                SET fix = EXCLUDED.fix, explanation = EXCLUDED.explanation, created_at = NOW()
                """,
                vuln_id, 
                fix_data.get("fixed_code"), 
                fix_data.get("explanation")
            )
            return True
        except Exception as e:
            print(f"Error saving fix proposal: {e}")
            return False
        finally:
            await conn.close()

    async def get_fix_proposal(self, vuln_id: str):
        conn = await self.get_connection()
        try:
            row = await conn.fetchrow("""
                SELECT * FROM fix_proposals WHERE vuln_id = $1
            """, vuln_id)
            return dict(row) if row else None
        finally:
            await conn.close()
