from pymongo import MongoClient
import logging
from app.config.settings import settings

logger = logging.getLogger("datalogger")

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None
        self.is_connected = False
    
    def connect(self):
        try:
            # Short timeout to detect offline mode quickly
            self.client = MongoClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=10000
            )
            self.db = self.client[settings.MONGODB_DB]
            # Test connexion
            self.client.admin.command('ping')
            self.is_connected = True
            print("✅ Connected to MongoDB")
        except Exception as e:
            self.is_connected = False
            print(f"❌ MongoDB Connection Failed: {e}")
            # In production, we might want to raise here, but for now we let it fail gracefully so health check returns 503
    
    def get_collection(self, name: str):
        if not self.is_connected:
             return None
        return self.db[name]

# Singleton
mongodb = MongoDB()
