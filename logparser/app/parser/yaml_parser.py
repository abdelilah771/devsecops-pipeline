import yaml

def parse_workflow(workflow_data: dict) -> dict:
    """Parse et normalise workflow GitHub Actions"""
    try:
        # Si c'est une string YAML, parser
        if isinstance(workflow_data, str):
            workflow_data = yaml.safe_load(workflow_data)
        
        # Extraire informations importantes
        parsed = {
            'name': workflow_data.get('name', 'unknown'),
            'permissions': workflow_data.get('permissions', {}),
            'jobs': {},
            'actions_used': [],
            'secrets_referenced': []
        }
        
        # Parser jobs
        jobs = workflow_data.get('jobs', {})
        for job_name, job_data in jobs.items():
            steps = job_data.get('steps', [])
            
            # Extraire actions
            for step in steps:
                if 'uses' in step:
                    parsed['actions_used'].append(step['uses'])
                
                # Extraire secrets
                if 'env' in step:
                    for key, value in step['env'].items():
                        if 'secrets.' in str(value):
                            parsed['secrets_referenced'].append(key)
            
            parsed['jobs'][job_name] = {
                'runs_on': job_data.get('runs-on'),
                'steps_count': len(steps)
            }
        
        return parsed
        
    except Exception as e:
        print(f"❌ Parse error: {e}")
        return {'error': str(e)}
