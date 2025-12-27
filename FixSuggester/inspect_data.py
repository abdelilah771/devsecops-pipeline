import asyncio
from app.services.postgres_service import PostgresService

async def inspect_data():
    service = PostgresService()
    conn = await service.get_connection()
    try:
        row = await conn.fetchrow("SELECT * FROM vulnerabilities LIMIT 1")
        if row:
            print("Row data:")
            for key, value in dict(row).items():
                print(f"{key}: {value}")
        else:
            print("No data in vulnerabilities table.")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(inspect_data())
