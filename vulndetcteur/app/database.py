from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pymongo import MongoClient
import os

# PostgreSQL
SQLALCHEMY_DATABASE_URL = os.getenv("POSTGRES_URI", "postgresql://postgres:root@localhost:5432/vulndetec")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MongoDB
# MongoDB - Standard Connection String (Bypassing SRV DNS Lookup)
# MongoDB - Standard Connection String (Bypassing SRV DNS Lookup) with increased timeouts AND TLS enabled
MONGO_URL = os.getenv("MONGO_URL", "mongodb://abdelilahdahou777_db_user:kfsPNTrukGyJxs9a@ac-tthnx18-shard-00-00.ns6lzot.mongodb.net:27017,ac-tthnx18-shard-00-01.ns6lzot.mongodb.net:27017,ac-tthnx18-shard-00-02.ns6lzot.mongodb.net:27017/?authSource=admin&replicaSet=atlas-v9kb86-shard-0&retryWrites=true&w=majority&appName=safeops-logminer&connectTimeoutMS=60000&serverSelectionTimeoutMS=60000&tls=true")
mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client["safeops-logminer"]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_mongo_db():
    return mongo_db
