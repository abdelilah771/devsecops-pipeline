
from pymongo import MongoClient
from app.config import settings

def check_coverage():
    client = MongoClient(settings.mongo_uri)
    db = client[settings.mongo_db]
    
    logs_col = db["Log"]
    events_col = db["ParsedEvents"]
    
    # Get all distinct run_ids from Logs
    run_ids = logs_col.distinct("run_id")
    print(f"--- DATABASE AUDIT ---")
    print(f"Total Unique Runs in 'Log': {len(run_ids)}")
    print("-" * 40)
    print(f"{'RUN_ID':<30} | {'LOG FOUND':<10} | {'PARSED EVENTS COUNT':<20}")
    print("-" * 40)
    
    for run_id in run_ids:
        # Check ParsedEvents count
        event_count = events_col.count_documents({"run_id": run_id})
        log_status = "✅"
        
        status_icon = "✅" if event_count > 0 else "⚠️ (Not parsed yet?)"
        
        print(f"{run_id:<30} | {log_status:<10} | {event_count:<5} {status_icon}")

if __name__ == "__main__":
    check_coverage()
