import os
import yaml
import click

POLICY_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'security_policy.yaml')

def load_security_policy():
    """Loads the security policy from the security_policy.yaml file."""
    if not os.path.exists(POLICY_FILE):
        click.echo(f"Warning: Security policy file not found at {POLICY_FILE}. Using default empty policy.", err=True)
        return {"compliance": {}, "disallowed_patterns": []}
    
    try:
        with open(POLICY_FILE, 'r') as f:
            policy = yaml.safe_load(f)
            return policy if policy is not None else {"compliance": {}, "disallowed_patterns": []}
    except yaml.YAMLError as e:
        click.echo(f"Error parsing security policy file {POLICY_FILE}: {e}", err=True)
        return {"compliance": {}, "disallowed_patterns": []}
