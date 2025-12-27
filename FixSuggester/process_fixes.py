import asyncio
import logging
from app.services.postgres_service import PostgresService
from app.services.fix_generator import FixGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    pg_service = PostgresService()
    fix_generator = FixGenerator()

    logger.info("Initializing database...")
    await pg_service.ensure_tables_exist()

    # Seed some test data if empty (Optional, strictly for testing purposes if user hasn't inserted any)
    # For now, we assume data might exist or we just wait. 
    # But to be helpful, let's insert a test vuln if none exist.
    conn = await pg_service.get_connection()
    try:
        count = await conn.fetchval("SELECT COUNT(*) FROM vulnerabilities")
        if count == 0:
            logger.info("Seeding test vulnerability...")
            await conn.execute("""
                INSERT INTO vulnerabilities (vuln_id, description, location)
                VALUES ('vuln-test-1', 'SQL Injection', '{"line_excerpt": "SELECT * FROM users WHERE name = " + user_input}')
                ON CONFLICT (vuln_id) DO NOTHING
            """)
    finally:
        await conn.close()

    logger.info("Fetching unprocessed vulnerabilities...")
    vulns = await pg_service.fetch_unprocessed_vulnerabilities()
    
    if not vulns:
        logger.info("No unprocessed vulnerabilities found.")
        return

    logger.info(f"Found {len(vulns)} vulnerabilities to process.")

    for vuln in vulns:
        # Map 'id' to 'vuln_id' for fix_generator
        vuln['vuln_id'] = vuln['id']
        logger.info(f"Processing vulnerability: {vuln['id']}")
        
        result = await fix_generator.generate_from_event(vuln)
        
        if result.get("error"):
            logger.error(f"Failed to generate fix for {vuln['id']}: {result['error']}")
        else:
            logger.info(f"Successfully generated and saved fix for {vuln['id']}. Source: {result.get('source')}")

if __name__ == "__main__":
    asyncio.run(main())
