import re

def parse_github_log(log_content: str):
    events = []
    # Regex to find job and step names
    job_pattern = re.compile(r"##\[group\]Run\s+(.*)")
    step_pattern = re.compile(r"^\s*###\s*(.*)")
    exit_code_pattern = re.compile(r"Completed with exit code (\d+)")

    current_job = "default_job"

    for line in log_content.splitlines():
        line = line.strip()
        if not line:
            continue
            
        if job_match := job_pattern.match(line):
            current_job = job_match.group(1)
            events.append({
                "model": "ParsedEvent",
                "event_type": "job", 
                "job_name": current_job,
                "message": f"Job started: {current_job}"
            })
        elif step_match := step_pattern.match(line):
            step_name = step_match.group(1)
            events.append({
                "model": "ParsedEvent",
                "event_type": "step", 
                "job_name": current_job,
                "step_name": step_name,
                "message": f"Step: {step_name}"
            })
        elif exit_code_match := exit_code_pattern.search(line):
            code = int(exit_code_match.group(1))
            status = "failed" if code != 0 else "success"
            events.append({
                "model": "ParsedEvent",
                "event_type": "exit_code", 
                "job_name": current_job,
                "status": status,
                "message": f"Exit code: {code}"
            })
        else:
            # Generic command output or log line
            events.append({
                "model": "ParsedEvent",
                "event_type": "command", 
                "job_name": current_job,
                "message": line
            })

    return events
