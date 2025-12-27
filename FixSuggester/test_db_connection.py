import asyncio
from app.services.postgres_service import PostgresService
from app.core.config import settings

async def test_connection():
    print(f"Testing connection to: {settings.POSTGRES_URI or 'configured components'}")
    service = PostgresService()
    try:
        conn = await service.get_connection()
        version = await conn.fetchval("SELECT version()")
        print(f"✅ Connection successful! Postgres Version: {version}")
        await conn.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())
