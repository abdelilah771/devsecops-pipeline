import csv
import argparse
import sys
import uuid
from datetime import datetime
from app.database import db
from app.parsers.github_parser import parse_github_log
from app.parsers.gitlab_parser import parse_gitlab_log
from app.parsers.jenkins_parser import parse_jenkins_log

def export_log_to_csv(run_id, provider, output_file=None):
    print(f"Fetching raw log for run_id: {run_id}...")
    raw_log = db.raw_logs.find_one({"run_id": run_id})
    
    if not raw_log:
        print(f"Error: No raw log found for run_id '{run_id}'.")
        return

    log_content = raw_log.get("log_content")
    if not log_content:
        print("Error: Log content is empty or missing.")
        return

    print(f"Parsing log with provider: {provider}...")
    events = []
    try:
        if provider == "github":
            events = parse_github_log(log_content)
        elif provider == "gitlab":
            events = parse_gitlab_log(log_content)
        elif provider == "jenkins":
            events = parse_jenkins_log(log_content)
        else:
            print(f"Error: Unknown provider '{provider}'. Supported: github, gitlab, jenkins")
            return
    except Exception as e:
        print(f"Error during parsing: {e}")
        return

    if not events:
        print("No events found in log.")
        return

    if not output_file:
        output_file = f"events_{run_id}.csv"

    print(f"Writing {len(events)} events to {output_file}...")
    
    fieldnames = ["event_id", "run_id", "type", "job_name", "step_name", "exit_code", "secret_hint", "url", "timestamp"]
    
    try:
        with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for event in events:
                # Normalize data to match the ParsedEvent model structure
                row = {
                    "event_id": str(uuid.uuid4()),
                    "run_id": run_id,
                    "type": event.get("type"),
                    "job_name": event.get("job_name"),
                    "step_name": event.get("step_name"),
                    "exit_code": event.get("exit_code"),
                    "secret_hint": event.get("secret_hint"),
                    "url": event.get("url"),
                    "timestamp": datetime.utcnow().isoformat()
                }
                writer.writerow(row)
                
        print("Done.")
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse a raw log from MongoDB and export to CSV.")
    parser.add_argument("run_id", help="The run_id of the log to parse")
    parser.add_argument("provider", choices=["github", "gitlab", "jenkins"], help="The CI provider (github, gitlab, jenkins)")
    parser.add_argument("--output", "-o", help="Output CSV file name", default=None)

    args = parser.parse_args()
    
    export_log_to_csv(args.run_id, args.provider, args.output)
