import os
import sys
import json
import uuid
import logging
from sqlalchemy import create_engine, text
from pymongo import MongoClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load .env manually since python-dotenv might not be installed
def load_env():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    if not os.environ.get(key):
                        os.environ[key] = value.strip().strip('"').strip("'")

load_env()

POSTGRES_URI = os.getenv("POSTGRES_URI", "postgresql://postgres:root@localhost:5432/vulndetec")
# Use the robust direct connection string from database.py as default if env var is missing or fails
ROBUST_MONGO = "mongodb://abdelilahdahou777_db_user:kfsPNTrukGyJxs9a@ac-tthnx18-shard-00-00.ns6lzot.mongodb.net:27017,ac-tthnx18-shard-00-01.ns6lzot.mongodb.net:27017,ac-tthnx18-shard-00-02.ns6lzot.mongodb.net:27017/?authSource=admin&replicaSet=atlas-v9kb86-shard-0&retryWrites=true&w=majority&appName=safeops-logminer&connectTimeoutMS=60000&serverSelectionTimeoutMS=60000&tls=true"
MONGODB_URI = os.getenv("MONGO_URL") or os.getenv("MONGODB_URI") or ROBUST_MONGO
MONGODB_DB = os.getenv("MONGODB_DB", "devsecops")

RUN_ID = "test_verification_001"

def verify_postgres():
    logger.info(f"Checking PostgreSQL connection...")
    try:
        engine = create_engine(POSTGRES_URI)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            logger.info("✅ PostgreSQL Connection Successful!")
    except Exception as e:
        logger.error(f"❌ PostgreSQL Connection Failed: {e}")
        # Non-critical for Mongo test, but critical for app.
        # sys.exit(1) 

def verify_and_seed_mongo():
    logger.info(f"Checking MongoDB connection...")
    try:
        # Increased timeout and use robust URI
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=10000, connectTimeoutMS=10000)
        db = client[MONGODB_DB]
        # Check connection
        client.admin.command('ping')
        logger.info("✅ MongoDB Connection Successful!")

        # Seed Data
        collection = db["ParsedEvents"]
        
        # Clean existing test data
        collection.delete_many({"run_id": RUN_ID})
        
        # Test Event with a secret leak to trigger detection
        test_event = {
            "run_id": RUN_ID,
            "event_id": str(uuid.uuid4()),
            "job_name": "build-job",
            "step_name": "checkout",
            "message": "AWS_ACCESS_KEY_ID=AKIA1234567890EXAMPLE", # Secret leak
            "timestamp": "2023-10-27T10:00:00Z"
        }
        
        # Unpinned action event
        test_event_2 = {
            "run_id": RUN_ID,
            "event_id": str(uuid.uuid4()),
            "job_name": "deploy-job",
            "step_name": "deploy",
            "message": "uses: actions/checkout@latest", # Unpinned action
            "timestamp": "2023-10-27T10:05:00Z"
        }

        collection.insert_many([test_event, test_event_2])
        logger.info(f"✅ Seeded MongoDB with 2 test events for run_id: {RUN_ID}")

    except Exception as e:
        logger.error(f"❌ MongoDB Connection Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify_postgres()
    verify_and_seed_mongo()
