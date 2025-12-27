
import httpx
import asyncio

async def check_health():
    url = "http://127.0.0.1:8001/"
    print(f"Checking {url}...")
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            print(f"Server reachable! Status: {resp.status_code}")
            print(f"Response: {resp.json()}")
    except Exception as e:
        print(f"Connection failed: {e}")

async def check_parse_route():
    url = "http://127.0.0.1:8001/parse"
    print(f"Checking methods for {url}...")
    try:
        async with httpx.AsyncClient() as client:
            # GET on POST-only route usually returns 405 Method Not Allowed
            resp = await client.get(url) 
            print(f"Route exists! Status: {resp.status_code} (Expected 405 if route exists but method wrong)")
    except Exception as e:
        print(f"Route check failed: {e}")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(check_health())
    loop.run_until_complete(check_parse_route())
