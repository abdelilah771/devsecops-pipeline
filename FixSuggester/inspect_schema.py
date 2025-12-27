import asyncio
from app.services.postgres_service import PostgresService

async def inspect():
    service = PostgresService()
    conn = await service.get_connection()
    try:
        rows = await conn.fetch("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'vulnerabilities';
        """)
        print("Columns in 'vulnerabilities' table:")
        for row in rows:
            print(f"- {row['column_name']}: {row['data_type']}")
            
        rows = await conn.fetch("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'fix_proposals';
        """)
        print("\nColumns in 'fix_proposals' table:")
        for row in rows:
            print(f"- {row['column_name']}: {row['data_type']}")

    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(inspect())
