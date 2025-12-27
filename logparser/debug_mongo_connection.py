import pymongo
import os
from dotenv import load_dotenv
import dns.resolver

load_dotenv()

uri = os.getenv("MONGODB_URI")
print(f"Testing connection to: {uri.split('@')[-1]}") # Hide credentials

try:
    print("Attempting to resolve DNS SRV record...")
    # Manual resolution test
    domain = uri.split('@')[-1].split('/')[0]
    try:
        answers = dns.resolver.resolve('_mongodb._tcp.' + domain, 'SRV')
        print("DNS SRV Resolution SUCCESS:")
        for rdata in answers:
            print(f" - {rdata.target}:{rdata.port}")
    except Exception as e:
        print(f"DNS SRV Resolution FAILED: {e}")

    print("\nAttempting pymongo connection (timeout=5s)...")
    client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("MongoDB Connection SUCCESS!")
except Exception as e:
    print(f"MongoDB Connection FAILED: {e}")
