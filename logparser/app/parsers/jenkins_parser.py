import re

def parse_jenkins_log(log_content: str):
    events = []
    # Regex to find pipeline stages and shell commands
    # stage_pattern = re.compile(r"\[Pipeline\] stage") # Simplified
    # Or matches: [Pipeline] stage: ... or just detecting the block.
    # The original regex was: re.compile(r"[Pipeline] stage\n(.*)")
    # Assuming the log line is like: "[Pipeline] stage" or "[Pipeline] { (Build)"
    
    # Let's try to capture meaningful info. 
    # If the line is "[Pipeline] { (Build)", we want "Build".
    stage_pattern = re.compile(r"\[Pipeline\]\s+\{\s+\((.*)\)") 
    sh_pattern = re.compile(r"\[Pipeline\]\s+sh") # detecting sh block start?
    # actually sh command execution often shows as:
    # [Pipeline] sh
    # + mvn clean install
    # The + line is the command.
    cmd_pattern = re.compile(r"^\+\s+(.*)")
    
    current_job = "jenkins_pipeline"

    for line in log_content.splitlines():
        line = line.strip()
        if not line:
            continue

    for line in log_content.splitlines():
        line = line.strip()
        if not line:
            continue

        if stage_match := stage_pattern.search(line):
            stage = stage_match.group(1).strip()
            events.append({
                "event_type": "job", 
                "job_name": stage,
                "message": f"Stage: {stage}"
            })
        elif cmd_match := cmd_pattern.match(line):
            cmd = cmd_match.group(1).strip()
            events.append({
                "event_type": "step", 
                "job_name": current_job,
                "step_name": cmd, 
                "message": f"Shell: {cmd}"
            })
        else:
             events.append({
                "event_type": "command", 
                "job_name": current_job,
                "message": line
            })

    return events
