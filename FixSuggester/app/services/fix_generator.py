from app.services.postgres_service import PostgresService
from app.services.redis_service import RedisService
from app.services.gemini_service import GeminiService
from app.services.prompt_service import PromptService

class FixGenerator:
    def __init__(self):
        self.pg = PostgresService()
        self.redis = RedisService()
        self.gemini = GeminiService()
        self.prompt = PromptService()

    async def generate_fix(self, vuln_id: str):
        # 1. Fetch Vulnerability
        vuln = await self.pg.get_vulnerability(vuln_id)
        if not vuln:
            return {"error": "Vulnerability not found"}

        # 2. Check Cache
        cached_fix = await self.redis.get_cached_fix(vuln_id)
        if cached_fix:
            return {"source": "cache", "fix": cached_fix}

        # 3. Generate with Gemini
        prompt = self.prompt.generate_prompt(vuln)
        fix = await self.gemini.generate_fix(prompt)

        # 4. Fallback if Gemini fails
        if not fix:
            fix = self._get_fallback_fix(vuln)
            source = "fallback"
        else:
            source = "llm"

        # 5. Cache Result
        await self.redis.cache_fix(vuln_id, fix)

        return {"source": source, "fix": fix}

        return {
            "fixed_code": "# Manual review required",
            "explanation": "Automated generation failed. Please review OWASP guidelines.",
            "steps": ["Assess risk", "Apply manual patch"]
        }

    async def generate_from_event(self, vuln_data: dict):
        """
        Processes a vulnerability event directly from RabbitMQ.
        """
        vuln_id = vuln_data.get("vuln_id")
        if not vuln_id:
            return {"error": "No vuln_id in event"}

        # 1. Check Cache
        cached_fix = await self.redis.get_cached_fix(vuln_id)
        if cached_fix:
            print(f"Fix for {vuln_id} found in cache.")
            return {"source": "cache", "fix": cached_fix}

        # 2. Generate with Gemini
        # We construct a prompt from the event data which is richer
        prompt = self.prompt.generate_prompt(vuln_data)
        fix = await self.gemini.generate_fix(prompt)

        # 3. Fallback
        if not fix:
            fix = self._get_fallback_fix(vuln_data)
            source = "fallback"
        else:
            source = "llm"

        # 4. Save Proposal to DB
        await self.pg.save_fix_proposal(vuln_id, fix)

        # 5. Cache Result
        await self.redis.cache_fix(vuln_id, fix)

        return {"source": source, "fix": fix}
