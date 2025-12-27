import redis.asyncio as redis
import json
from app.core.config import settings

class RedisService:
    def __init__(self):
        if not settings.MOCK_REDIS:
            self.redis = redis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", decode_responses=True)
        self.ttl = 3600  # 1 hour TTL

    async def get_cached_fix(self, vuln_id: str):
        if settings.MOCK_REDIS:
            return None
        data = await self.redis.get(f"fix:{vuln_id}")
        return json.loads(data) if data else None

    async def cache_fix(self, vuln_id: str, fix_data: dict):
        if settings.MOCK_REDIS:
            return
        await self.redis.setex(f"fix:{vuln_id}", self.ttl, json.dumps(fix_data))
