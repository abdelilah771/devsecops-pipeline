from pymongo import MongoClient
from app.config import settings

def check_db():
    print(f"Connecting to MongoDB...")
    print(f"URI: {settings.mongo_uri}")
    print(f"Target DB: {settings.mongo_db}")

    try:
        client = MongoClient(settings.mongo_uri)
        # Force a connection check
        client.admin.command('ping')
        print("Connection successful!")
        
        db = client[settings.mongo_db]
        
        print("\nCollections in database:")
        collections = db.list_collection_names()
        print(collections)
        
        if not collections:
            print("WARNING: No collections found in this database.")
            
        for col_name in collections:
            count = db[col_name].count_documents({})
            print(f" - {col_name}: {count} documents")
            
            if count > 0:
                print(f"   Sample document from {col_name}:")
                print(db[col_name].find_one())

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    check_db()
