def extract_security_features(parsed_workflow: dict) -> dict:
    """Extrait features pour détection ML"""
    
    features = {
        # Permissions
        'has_write_all': parsed_workflow.get('permissions') == 'write-all',
        'permissions_count': len(parsed_workflow.get('permissions', {})) if isinstance(parsed_workflow.get('permissions'), dict) else 0,
        
        # Actions
        'total_actions': len(parsed_workflow.get('actions_used', [])),
        'unpinned_actions': sum(1 for action in parsed_workflow.get('actions_used', []) if '@' not in action or not action.split('@')[1].startswith('v')),
        
        # Secrets
        'secrets_count': len(parsed_workflow.get('secrets_referenced', [])),
        'secrets_in_run': any('run' in step for step in parsed_workflow.get('jobs', {}).values()),
        
        # Jobs
        'jobs_count': len(parsed_workflow.get('jobs', {})),
    }
    
    return features
