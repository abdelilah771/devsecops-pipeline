import re

def parse_gitlab_log(log_content: str):
    events = []
    # Regex to find command executions
    command_pattern = re.compile(r"^\$\s+(.*)")
    
    current_job = "gitlab_job" # GitLab logs might rely on the filename or other metadata for job name, using default here.

    for line in log_content.splitlines():
        line = line.strip()
        if not line:
            continue

        if command_match := command_pattern.match(line):
            cmd = command_match.group(1)
            events.append({
                "event_type": "step", 
                "job_name": current_job,
                "step_name": cmd, 
                "message": f"Executing: {cmd}"
            })
        else:
            events.append({
                "event_type": "command",
                "job_name": current_job, 
                "message": line
            })

    return events
