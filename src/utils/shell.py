import subprocess

def run_shell_command(command: str):
    """Runs a shell command and returns its stdout, stderr, and return code."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=False)
        return {
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "returncode": 1
        }
