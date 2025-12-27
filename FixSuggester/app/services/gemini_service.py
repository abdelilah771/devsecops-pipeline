from google import genai
from app.core.config import settings
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_name = "gemini-3-flash-preview"  # Explicit user request

    async def generate_fix(self, prompt: str):
        if settings.MOCK_AI:
            # Simple keyword matching to simulate LLM understanding
            if "SQL Injection" in prompt:
                return {
                    "fixed_code": "query = 'SELECT * FROM users WHERE username = %s'\ncursor.execute(query, (username,))",
                    "explanation": "Used parameterized query to prevent SQL injection.",
                    "steps": ["Replace string concatenation with placeholder", "Pass parameters as tuple"]
                }
            elif "XSS" in prompt:
                return {
                    "fixed_code": "import html\nreturn f'<h1>Search results for: {html.escape(user_input)}</h1>'",
                    "explanation": "Escaped user input using html.escape() to prevent XSS.",
                    "steps": ["Import html module", "Wrap user input in escape function"]
                }
            elif "Hardcoded" in prompt:
                return {
                    "fixed_code": "import os\nAWS_KEY = os.getenv('AWS_ACCESS_KEY_ID')",
                    "explanation": "Moved secret to environment variable.",
                    "steps": ["Remove hardcoded string", "Use os.getenv to read from environment"]
                }
            else:
                 return {
                    "fixed_code": "# Mocked Generic Fix",
                    "explanation": "Generic fix for unknown vulnerability type.",
                    "steps": ["Manual review required"]
                }

        try:
            logger.info(f"Generating fix with model: {self.model_name}")
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            
            text = response.text.strip()
            # Basic JSON extraction
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
                
            return json.loads(text)
        except Exception as e:
            logger.error(f"Gemini API Error: {str(e)}")
            return None
