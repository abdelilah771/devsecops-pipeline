
import asyncio
import httpx
from pymongo import MongoClient
from datetime import datetime
from app.config import settings

import uuid

# ---------------- CONFIGURATION ----------------
API_URL = "http://127.0.0.1:8001/parse"
RUN_ID = f"auto_test_{uuid.uuid4().hex[:8]}"
PROVIDER = "GITHUB"
# -----------------------------------------------

def setup_test_data():
    """
    Insère un log fictif dans MongoDB pour que l'API puisse le trouver.
    """
    print(f"--- 1. Préparation des données (MongoDB) ---")
    client = MongoClient(settings.mongo_uri)
    db = client[settings.mongo_db]
    logs_col = db["Log"]

    # Nettoyage
    logs_col.delete_many({"run_id": RUN_ID})

    # Insertion d'un log exemple
    log_content = """##[group]Run actions/checkout@v2
### Checkout
Completed with exit code 0
"""
    log_doc = {
        "run_id": RUN_ID,
        "provider": PROVIDER,
        "repo_name": "client/test-repo",
        "log_data": log_content,
        "timestamp_received": datetime.utcnow(),
        "pipeline_name": "test-pipeline",
        "author": "client-user"
    }
    logs_col.insert_one(log_doc)
    print(f"✅ Log inséré avec Run ID: {RUN_ID}")

async def call_api():
    """
    Appelle l'API LogParser comme le ferait un client.
    """
    print(f"\n--- 2. Appel API (Client) ---")
    print(f"POST {API_URL}")
    payload = {"run_id": RUN_ID, "provider": PROVIDER}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(API_URL, json=payload)
            print(f"Status Code: {response.status_code}")
            print(f"Réponse JSON: {response.json()}")
            
            if response.status_code == 200:
                print("\n✅ SUCCÈS : Le log a été parsé et envoyé à RabbitMQ.")
            else:
                print("\n❌ ÉCHEC : L'API a retourné une erreur.")
        except Exception as e:
            print(f"\n❌ ERREUR DE CONNEXION : {e}")
            print("Assurez-vous que le serveur tourne bien sur le port 8001.")

if __name__ == "__main__":
    setup_test_data()
    asyncio.run(call_api())
