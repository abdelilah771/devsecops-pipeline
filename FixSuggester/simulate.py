import asyncio
import time
from app.services.fix_generator import FixGenerator

async def simulate():
    print("🚀 Starting FixSuggester Simulation (MOCK_MODE)...\n")
    generator = FixGenerator()
    
    scenarios = [
        ("vuln-sqli", "SQL Injection"),
        ("vuln-xss", "Cross-Site Scripting (XSS)"),
        ("vuln-secret", "Hardcoded Secret")
    ]

    for vuln_id, label in scenarios:
        print(f"--- Processing {label} ({vuln_id}) ---")
        result = await generator.generate_fix(vuln_id)
        
        fix = result.get("fix", {})
        print(f"🔌 Source: {result.get('source')}")
        print(f"📝 Explanation: {fix.get('explanation')}")
        print(f"🛠️  Code Fix:\n{fix.get('fixed_code')}")
        print("\n" + "="*50 + "\n")
        print("⏳ Waiting 10s to respect API rate limits...")
        time.sleep(10)

if __name__ == "__main__":
    asyncio.run(simulate())
