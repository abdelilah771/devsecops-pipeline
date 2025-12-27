import asyncio
from app.services.postgres_service import PostgresService

async def verify_saved_fixes():
    service = PostgresService()
    conn = await service.get_connection()
    try:
        rows = await conn.fetch("SELECT * FROM fix_proposals ORDER BY created_at DESC LIMIT 5")
        print(f"Found {len(rows)} fix proposals:")
        for row in rows:
            print(f"\n--- Fix for {row['vuln_id']} ---")
            print(f"Explanation: {row['explanation'][:100]}...")
            print(f"Fix Snippet: {row['fix'][:50]}...")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(verify_saved_fixes())
