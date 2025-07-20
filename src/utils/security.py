import click
import os
import shutil
import subprocess
import tempfile
import json
import asyncio
from datetime import datetime
from urllib.parse import urlparse
from functools import wraps
from dotenv import load_dotenv

class CredentialManager:
    def __init__(self):
        load_dotenv()  # Load from .env file
        self.secrets = {
            "GOOGLE_API": os.getenv("GOOGLE_API_KEY", ""),
            "OPENAI_API": os.getenv("OPENAI_API_KEY", "")
        }

    def get_key(self, service_name):
        return self.secrets.get(service_name, "")


def validate_url(url):
    """Strict URL validation with scheme verification"""
    parsed = urlparse(url)
    if not parsed.scheme or parsed.scheme not in ["http", "https"]:
        raise ValueError(f"Invalid URL scheme: {url}")
    if not parsed.netloc:
        raise ValueError(f"Missing domain in URL: {url}")
    return url

def sanitized_url(func):
    """Decorator for URL sanitization"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'url' in kwargs:
            kwargs['url'] = validate_url(kwargs['url'])
        return func(*args, **kwargs)
    return wrapper

def safe_exec(code: str):
    """Execute AI-generated patches securely within a restricted environment."""
    compiled = compile_restricted(code, '<string>', 'exec')
    restricted_globals = {"__builtins__": safe_builtins}
    exec(compiled, restricted_globals)

async def run_in_sandbox(command: list, target_path: str, description: str = "Running command in sandbox"):
    """
    Executes a shell command in a temporary, isolated directory asynchronously.
    Copies the target_path (file or directory) into the sandbox before execution.
    """
    with tempfile.TemporaryDirectory() as sandbox_dir:
        click.echo(f"[*] {description} in isolated sandbox: {sandbox_dir}")
        
        # Determine if target_path is a file or directory
        if os.path.isfile(target_path):
            shutil.copy(target_path, sandbox_dir)
            # Adjust command to refer to the copied file in the sandbox
            # This assumes the command expects a file path as its last argument
            command[-1] = os.path.join(sandbox_dir, os.path.basename(target_path))
        elif os.path.isdir(target_path):
            # Copy directory contents
            for item in os.listdir(target_path):
                s = os.path.join(target_path, item)
                d = os.path.join(sandbox_dir, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)
            # Adjust command to refer to the copied directory in the sandbox
            command[-1] = sandbox_dir
        else:
            raise ValueError(f"Target path is neither a file nor a directory: {target_path}")

        # Execute the command in the sandbox directory asynchronously
        try:
            process = await asyncio.create_subprocess_exec(
                *command,
                cwd=sandbox_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=os.environ.copy()
            )
            stdout, stderr = await process.communicate()
            return stdout.decode(), stderr.decode(), process.returncode
        except FileNotFoundError:
            return "", f"Error: Command '{command[0]}' not found in sandbox environment.", 127

def log_feedback(finding_details: dict, suggested_fix: str, applied: bool):
    """Logs feedback on AI-suggested fixes to a file."""
    feedback_entry = {
        "timestamp": datetime.now().isoformat(),
        "finding": finding_details,
        "suggested_fix": suggested_fix,
        "applied": applied
    }
    feedback_file = os.path.join(os.path.expanduser('~'), '.bughunter_feedback.log')
    with open(feedback_file, 'a') as f:
        f.write(json.dumps(feedback_entry) + '\n')
    click.echo("[*] Feedback logged.")

def log_audit_event(user: str, action: str, metadata: dict = None):
    """Logs an audit event to a file."""
    audit_entry = {
        "timestamp": datetime.now().isoformat(),
        "user": user,
        "action": action,
        "metadata": metadata if metadata is not None else {}
    }
    audit_file = os.path.join(os.path.expanduser('~'), '.bughunter_audit.log')
    with open(audit_file, 'a') as f:
        f.write(json.dumps(audit_entry) + '\n')
