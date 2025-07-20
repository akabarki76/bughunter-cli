import click
import os
import shutil
import glob
import subprocess
import requests
import google.generativeai as genai
from github import Github
from dotenv import load_dotenv
import json
import difflib

import yaml
import asyncio
from src.tools import TOOL_REGISTRY
from src.tools.refactor import refactor
from src.tools.learn import learn
from src.tools import nmap, nikto, dirsearch, sqlmap, waybackurls, nuclei
from src.tools.pullpush import pullpush as pullpush_command



from src.utils.security import validate_url, run_in_sandbox, log_feedback, log_audit_event
from src.utils.cache_utils import get_vulnerability_data
from src.utils.policy_manager import load_security_policy
from src.workflow_engine import execute_workflow

SECURITY_POLICY = load_security_policy()

load_dotenv()

# Configure Gemini API
gemini_api_key = os.getenv("GEMINI_API_KEY")
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)

CONFIG_FILE = os.path.join(os.path.expanduser('~'), '.bughunter_config')

def save_github_token(token):
    with open(CONFIG_FILE, 'w') as f:
        f.write(f'github_token={token}\n')
    click.echo('GitHub token saved successfully.')

def load_github_token():
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, 'r') as f:
        for line in f:
            if line.startswith('github_token='):
                return line.strip().split('=')[1]
    return None

from src.utils.security import validate_url
from src.utils.ai_utils import call_ai_api

def find_subdomains(target):
    """Finds subdomains of a target domain using crt.sh."""
    try:
        url = f'https://crt.sh/?q=%.{target}&output=json'
        validate_url(url)
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes

        subdomains = set()
        for entry in response.json():
            name_value = entry.get('name_value', '')
            if name_value:
                # crt.sh returns multiple lines for some certs, split them
                for subdomain in name_value.split('\n'):
                    # Remove wildcard prefixes
                    if subdomain.startswith('*.'):
                        subdomain = subdomain[2:]
                    subdomains.add(subdomain.strip())
        return sorted(list(subdomains))

    except requests.exceptions.RequestException as e:
        click.echo(f'Error connecting to crt.sh: {e}', err=True)
        return None
    except ValueError:
        click.echo('Error parsing JSON response from crt.sh.', err=True)
        return None

@click.group()
def cli():
    pass

@cli.command()
@click.argument("tool_name")
@click.argument("target")
@click.option("-o", "--output", help="Output file")
@click.option("-p", "--ports", default="1-1000", help="Port range for nmap")
def run_tool(tool_name, target, output, **kwargs):
    """Run security tools"""
    if tool_name not in TOOL_REGISTRY:
        click.echo(f"Tool not supported: {tool_name}")
        return
    
    try:
        tool = TOOL_REGISTRY[tool_name]()
        result = tool.run(target, output_file=output, **kwargs)
        click.echo(result)
    except Exception as e:
        click.echo(f"Error: {str(e)}")


@cli.command()
@click.option('--name', default='World', help='Name to greet.')
def hello(name):
    click.echo(f'Hello, {name}!')

@cli.command()
@click.option('--source', default='default', help='Source to pull from.')
def pull(source):
    click.echo(f'Pulling data from {source}...')

@cli.command()
@click.option('--destination', default='default', help='Destination to push to.')
def push(destination):
    click.echo(f'Pushing data to {destination}...')

@cli.command()
@click.argument('tag_name')
@click.option('--message', '-m', default='', help='An optional message for the tag.')
def tag(tag_name, message):
    if message:
        click.echo(f'Tagging with {tag_name} and message: "{message}"...')
    else:
        click.echo(f'Tagging with {tag_name}...')

@cli.command()
@click.argument('item_id')
@click.argument('label_name')
@click.option('--action', default='add', type=click.Choice(['add', 'remove']), help='Action to perform (add or remove).')
def label(item_id, label_name, action):
    click.echo(f'{action.capitalize()}ing label "{label_name}" to item {item_id}...')

@cli.command()
@click.argument('user_type')
@click.option('--verbose', is_flag=True, help='Show verbose onboarding steps.')
def onboard(user_type, verbose):
    click.echo(f'Starting onboarding for {user_type}...')
    if verbose:
        click.echo('  - Step 1: Configure user settings')
        click.echo('  - Step 2: Install necessary tools')
        click.echo('  - Step 3: Provide access credentials')
    click.echo(f'Onboarding for {user_type} complete.')

@cli.group()
def github():
    pass

@github.command()
def init():
    """Initialize GitHub integration by setting up authentication."""
    token = click.prompt('Please enter your GitHub Personal Access Token', hide_input=True)
    save_github_token(token)
    log_audit_event("github_init", "GitHub integration initialized", {})

@github.group()
def pr():
    """Commands for interacting with GitHub Pull Requests."""
    pass

@pr.command()
@click.option('--repo', required=True, help='The GitHub repository (e.g., owner/repo).')
@click.option('--title', required=True, help='The title of the pull request.')
@click.option('--head', required=True, help='The name of the branch where your changes are implemented.')
@click.option('--base', default='main', help='The name of the branch you want to merge your changes into.')
def create(repo, title, head, base):
    """Creates a new pull request on GitHub."""
    token = load_github_token()
    if not token:
        click.echo("Error: GitHub Personal Access Token not found. Please run 'bughunter github init' first.", err=True)
        return

    log_audit_event("github_pr_create", f"GitHub PR creation initiated for {repo}", {"repo": repo, "title": title, "head": head, "base": base})

    try:
        g = Github(token)
        # Assuming the repo is in the format 'owner/repo_name'
        owner, repo_name = repo.split('/')
        repository = g.get_user().get_repo(repo_name) # This assumes the token belongs to the owner
        # Alternatively, for any public repo: repository = g.get_repo(repo)

        pull_request = repository.create_pull(
            title=title,
            body="Created by bughunter-cli", # You can add a body option later
            head=head,
            base=base
        )
        click.echo(f"Successfully created pull request: {pull_request.html_url}")
    except Exception as e:
        click.echo(f"Error creating pull request: {e}", err=True)

@github.group()
def issues():
    """Commands for interacting with GitHub Issues."""
    pass

@issues.command()
@click.option('--repo', required=True, help='The GitHub repository (e.g., owner/repo).')
@click.option('--state', default='open', type=click.Choice(['open', 'closed', 'all']), help='State of the issues to pull.')
def pull(repo, state):
    """Pulls issues from a GitHub repository."""
    click.echo(f'Pulling {state} issues from {repo}...')
    token = load_github_token()
    if not token:
        click.echo("Error: GitHub Personal Access Token not found. Please run 'bughunter github init' first.", err=True)
        return

    log_audit_event("github_issues_pull", f"GitHub issues pull initiated for {repo} with state {state}", {"repo": repo, "state": state})

    try:
        g = Github(token)
        owner, repo_name = repo.split('/')
        repository = g.get_user().get_repo(repo_name)
        
        issues = repository.get_issues(state=state)
        for issue in issues:
            click.echo(f'  #{issue.number}: {issue.title} (State: {issue.state})')
    except Exception as e:
        click.echo(f"Error pulling issues: {e}", err=True)

@github.group()
def comments():
    """Commands for interacting with GitHub comments."""
    pass

@comments.command()
@click.option('--repo', required=True, help='The GitHub repository (e.g., owner/repo).')
@click.option('--issue', type=int, required=True, help='The issue or pull request number.')
@click.option('--body', required=True, help='The comment body.')
def push(repo, issue, body):
    """Pushes a comment to a GitHub issue or pull request."""
    click.echo(f'Pushing comment to {repo}#{issue}...')
    token = load_github_token()
    if not token:
        click.echo("Error: GitHub Personal Access Token not found. Please run 'bughunter github init' first.", err=True)
        return

    try:
        g = Github(token)
        owner, repo_name = repo.split('/')
        repository = g.get_user().get_repo(repo_name)
        
        issue_obj = repository.get_issue(issue)
        issue_obj.create_comment(body)
        click.echo('Comment pushed successfully.')
    except Exception as e:
        click.echo(f"Error pushing comment: {e}", err=True)

@cli.command()
def autoclean():

    """Cleans up temporary files and build artifacts."""
    click.echo("Starting autoclean...")

    # Directories to clean
    cleanup_dirs = ['dist', 'build']
    
    # Find __pycache__ directories
    pycache_dirs = glob.glob('**__pycache__', recursive=True)
    cleanup_dirs.extend(pycache_dirs)

    for d in cleanup_dirs:
        if os.path.exists(d):
            click.echo(f'Deleting {d}...')
            shutil.rmtree(d)
        else:
            click.echo(f'{d} not found, skipping.')

    # Handle virtual environment separately with confirmation
    if os.path.exists('venv'):
        if click.confirm('Do you want to delete the virtual environment (venv)? This will remove all installed packages.'):
            click.echo('Deleting venv/...')
            shutil.rmtree('venv')
        else:
            click.echo('Skipping venv deletion.')
    else:
        click.echo('venv not found, skipping.')

    click.echo("Autoclean complete.")

@cli.group()
def report():
    """Commands for reporting."""
    pass

@report.group()
def result():
    """Commands for managing scan results."""
    pass

@result.command()
@click.argument('scan_file_path')
def scan(scan_file_path):
    """Reports on a scan result file."""
    click.echo(f'Reporting on scan result from: {scan_file_path}')
    click.echo(' (This is a placeholder for actual scan result parsing and reporting.)')

@cli.group()
def publish():
    """Commands for publishing the package."""
    pass

@publish.command('do')
@click.option('--repository', default='pypi', help='The repository to publish to (e.g., pypi, testpypi).')
def publish_do(repository):
    """Publishing the package to a specified repository (e.g., PyPI)."""
    click.echo(f'Publishing package to {repository}...')
    
    # Ensure packages are built first
    click.echo('Ensuring packages are built...')
    try:
        subprocess.run(['python', '-m', 'build'], check=True, capture_output=True)
        click.echo('Packages built successfully.')
    except subprocess.CalledProcessError as e:
        click.echo(f'Error building packages: {e.stderr.decode()}', err=True)
        return

    # Construct the twine command
    twine_command = ['twine', 'upload', 'dist/*']
    if repository != 'pypi':
        twine_command.extend(['--repository', repository])

    click.echo(f'Running: {' '.join(twine_command)}')
    try:
        subprocess.run(twine_command, check=True)
        click.echo('Package published successfully!')
    except subprocess.CalledProcessError as e:
        click.echo(f'Error publishing package: {e.stderr.decode()}', err=True)
    except FileNotFoundError:
        click.echo('Error: twine not found. Make sure it\'s installed in your virtual environment.', err=True)

@publish.command('init')
def publish_init():
    """Initializes publishing credentials for PyPI/TestPyPI."""
    click.echo("To publish your package, you need to provide your PyPI/TestPyPI credentials.")
    click.echo("The recommended way is to set environment variables:")
    click.echo("  export TWINE_USERNAME=\"__token__\"")
    click.echo("  export TWINE_PASSWORD=\"your_pypi_api_token\"")
    click.echo("Replace 'your_pypi_api_token' with your actual API token from PyPI or TestPyPI.")
    click.echo("For TestPyPI, the repository URL is https://test.pypi.org/legacy/")
    click.echo("Once set, you can run: bughunter publish [--repository testpypi]")

@cli.command()
@click.argument('scan_file_path')
def test_after_scan(scan_file_path):
    """Runs tests after performing a scan."""
    click.echo(f'--- Running scan for: {scan_file_path} ---')
    # Simulate scan reporting (as per bughunter report result scan)
    click.echo(' (This is a placeholder for actual scan result parsing and reporting.)')
    click.echo('Scan simulation complete.')

    click.echo('\n--- Running tests ---')
    try:
        # Ensure virtual environment is activated for pytest
        # This assumes the virtual environment is named 'venv' or '.venv'
        # and is in the project root.
        # For a more robust solution, you might need to locate the venv dynamically.
        pytest_command = [os.path.join(os.getcwd(), 'venv', 'bin', 'pytest')] # Assuming venv is in project root
        if not os.path.exists(pytest_command[0]):
            pytest_command = [os.path.join(os.getcwd(), '.venv', 'bin', 'pytest')] # Try .venv
        if not os.path.exists(pytest_command[0]):
            click.echo("Error: pytest executable not found in venv or .venv. Please ensure your virtual environment is set up correctly.", err=True)
            return

        subprocess.run(pytest_command, check=True)
        click.echo('Tests passed successfully!')
    except subprocess.CalledProcessError as e:
        click.echo(f'Tests failed: {e}', err=True)
    except FileNotFoundError:
        click.echo('Error: pytest not found. Make sure it\'s installed in your virtual environment.', err=True)

@cli.group()
def scan():
    """Commands for scanning targets."""
    pass

@scan.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--autocorrect', is_flag=True, help='Automatically correct found vulnerabilities.')
def code(path, autocorrect):
    """Scans a file or directory for vulnerabilities and optionally autocorrects them."""
    async def _code_async(path, autocorrect):
        click.echo(f"[*] Scanning {path} with Semgrep...")
        log_audit_event("scan_code", f"Code scan initiated for {path}", {"path": path, "autocorrect": autocorrect})
        
        semgrep_cmd = ["semgrep", "scan", "--json", "--config", "auto", path]
        
        try:
            stdout, stderr, returncode = await run_in_sandbox(semgrep_cmd, path, description=f"Scanning {path} with Semgrep")
            if returncode not in [0, 1]: # Semgrep exits 1 if findings are found
                click.echo(f"Error during Semgrep scan:\n{stderr}", err=True)
                return
                
            findings = json.loads(stdout)
            
            if not findings['results']:
                click.echo("[+] No vulnerabilities found.")
                return

            click.echo(f"[!] Found {len(findings['results'])} vulnerabilities.")

            if not autocorrect:
                for finding in findings['results']:
                    click.echo(f"""
- Rule: {finding['check_id']}
  File: {finding['path']}:{finding['start']['line']}
  Message: {finding['extra']['message']}
""")
                
                # Check for disallowed patterns
                with open(path, 'r') as f:
                    full_code_content = f.read()
                for pattern in SECURITY_POLICY.get("disallowed_patterns", []):
                    if pattern in full_code_content:
                        click.echo(f"""
[!] Policy Violation: Disallowed pattern '{pattern}' found in {path}""", err=True)
                return

            # Autocorrect logic
            click.echo("[*] Starting AI-powered autocorrection...")
            for finding in findings['results']:
                file_path = finding['path']
                start_line = finding['start']['line']
                end_line = finding['end']['line']
                rule_message = finding['extra']['message']
                
                with open(file_path, 'r') as f:
                    file_lines = f.readlines()

                vulnerable_snippet = "".join(file_lines[start_line - 1:end_line])
                
                file_extension = os.path.splitext(file_path)[1].lstrip('.')
                prompt = f"""
The following {file_extension} code snippet from the file '{file_path}' has a vulnerability (Rule ID: {finding['check_id']}):
'{rule_message}'

Vulnerable code:
```
{vulnerable_snippet}
```

Rewrite the vulnerable code snippet to fix the issue while maintaining its original functionality and style.
Return only the corrected code block, without any explanation or markdown formatting.
"""
                
                click.echo(f"\n[*] Analyzing vulnerability in {file_path}:{start_line}...")
                suggested_fix = call_ai_api(prompt).strip()

                # Clean up the suggestion if it's wrapped in markdown
                if suggested_fix.startswith("```") and suggested_fix.endswith("```"):
                    suggested_fix = "\n".join(suggested_fix.split('\n')[1:-1])

                click.echo("[*] AI has suggested a fix. Please review the changes:")
                
                diff = difflib.unified_diff(
                    vulnerable_snippet.splitlines(keepends=True),
                    suggested_fix.splitlines(keepends=True),
                    fromfile='Original',
                    tofile='Patched',
                )
                
                for line in diff:
                    if line.startswith('+'):
                        click.secho(line, fg='green', nl=False)
                    elif line.startswith('-'):
                        click.secho(line, fg='red', nl=False)
                    else:
                        click.echo(line, nl=False)

                if click.confirm('\nDo you want to apply this patch?'):
                    # Apply the patch
                    new_file_lines = file_lines[:start_line - 1] + suggested_fix.splitlines(keepends=True) + file_lines[end_line:]
                    with open(file_path, 'w') as f:
                        f.writelines(new_file_lines)
                    click.echo(f"[*] Patch applied to {file_path}")
                    log_feedback(finding, suggested_fix, True)
                else:
                    click.echo("[*] Patch skipped.")
                    log_feedback(finding, suggested_fix, False)

        except FileNotFoundError:
            click.echo("Error: semgrep is not installed. Please install it to use this feature.", err=True)
        except json.JSONDecodeError:
            click.echo(f"Error parsing Semgrep JSON output.", err=True)
        except Exception as e:
            click.echo(f"An unexpected error occurred: {e}", err=True)
    asyncio.run(_code_async(path, autocorrect))


@scan.command()
@click.argument('path', type=click.Path(exists=True))
def dependencies(path):
    """Scans project dependencies for known vulnerabilities using OSV-Scanner."""
    async def _dependencies_async(path):
        click.echo(f"[*] Scanning dependencies in {path} with OSV-Scanner...")
        log_audit_event("scan_dependencies", f"Dependency scan initiated for {path}", {"path": path})

        if not shutil.which("osv-scanner"):
            click.echo("Error: osv-scanner is not installed. Please install it to use this feature.", err=True)
            click.echo("See installation instructions at https://google.github.io/osv-scanner/")
            return

        cmd = ["osv-scanner", "--json", path]

        try:
            stdout, stderr, returncode = await run_in_sandbox(cmd, path, description=f"Scanning dependencies in {path} with OSV-Scanner")

            if returncode != 0 and returncode != 1:
                 click.echo(f"Error during OSV-Scanner execution:\n{stderr}", err=True)
                 return

            if not stdout.strip():
                click.echo("[+] No vulnerabilities found.")
                return

            data = json.loads(stdout)

            if not data.get('results'):
                click.echo("[+] No vulnerabilities found.")
                return

            click.echo("[!] Found vulnerabilities:")
            for res in data['results']:
                for pkg_vulns in res.get('packages', []):
                    pkg_name = pkg_vulns['package']['name']
                    for vuln in pkg_vulns.get('vulnerabilities', []):
                        vuln_id = vuln['id']
                        vuln_summary = vuln.get('summary', 'No summary available.')
                        click.echo(f"\n- Vulnerability: {vuln_id}")
                        click.echo(f"  Package: {pkg_name}")
                        click.echo(f"  Summary: {vuln_summary}")
                        affected_versions = [v['versions'] for v in vuln.get('affected', [])]
                        click.echo(f"  Affected Versions: {affected_versions}")

        except FileNotFoundError:
            click.echo("Error: osv-scanner is not installed.", err=True)
        except json.JSONDecodeError:
            click.echo("Error: Could not parse JSON output from OSV-Scanner.", err=True)
            click.echo(f"Raw output:\n{stdout}") # Use stdout here, not result.stdout
        except Exception as e:
            click.echo(f"An unexpected error occurred: {e}", err=True)
    asyncio.run(_dependencies_async(path))

@scan.command('c-cpp')
@click.argument('path', type=click.Path(exists=True))
def c_cpp(path):
    """Scans C/C++ code for vulnerabilities using cppcheck."""
    async def _c_cpp_async(path):
        click.echo(f"[*] Scanning {path} with cppcheck...")
        log_audit_event("scan_c_cpp", f"C/C++ scan initiated for {path}", {"path": path})

        if not shutil.which("cppcheck"):
            click.echo("Error: cppcheck is not installed. Please install it to use this feature.", err=True)
            click.echo("On Debian/Ubuntu, run: sudo apt-get install cppcheck")
            return

        cmd = ["cppcheck", "--enable=all", path]

        try:
            # cppcheck writes its findings to stderr, so we capture it
            stdout, stderr, returncode = await run_in_sandbox(cmd, path, description=f"Scanning {path} with cppcheck")
            
            if stderr:
                click.echo("[!] cppcheck found the following issues:")
                click.echo(stderr)
            else:
                click.echo("[+] No issues found by cppcheck.")

        except FileNotFoundError:
            click.echo("Error: cppcheck is not installed.", err=True)
        except Exception as e:
            click.echo(f"An unexpected error occurred: {e}", err=True)
    asyncio.run(_c_cpp_async(path))

@scan.command()
@click.argument("target")
@click.option("--top-ports", help="Scan top N ports (default: 100)", default=100)
def ports(target, top_ports):
    """Scan open ports on a target."""
    if not shutil.which("nmap"):
        click.echo("Error: nmap is not installed. Please install it to use this feature.", err=True)
        return
    cmd = ["nmap", "--top-ports", str(top_ports), "-T4", target]
    result = subprocess.run(cmd, capture_output=True, text=True)
    click.echo(result.stdout)

@scan.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--autocorrect', is_flag=True, help='Automatically correct found web vulnerabilities.')
def web(path, autocorrect):
    """Scans a web project for vulnerabilities using a targeted Semgrep ruleset."""
    async def _web_async(path, autocorrect):
        click.echo(f"[*] Scanning {path} for web vulnerabilities with Semgrep...")
        log_audit_event("scan_web", f"Web scan initiated for {path}", {"path": path, "autocorrect": autocorrect})
        
        semgrep_cmd = ["semgrep", "scan", "--json", "--config", "r/owasp-top-ten", path]
        
        try:
            stdout, stderr, returncode = await run_in_sandbox(semgrep_cmd, path, description=f"Scanning {path} for web vulnerabilities with Semgrep")
            if returncode not in [0, 1]:
                click.echo(f"Error during Semgrep scan:\n{stderr}", err=True)
                return
                
            findings = json.loads(stdout)
            
            if not findings['results']:
                click.echo("[+] No web vulnerabilities found.")
                return

            click.echo(f"[!] Found {len(findings['results'])} potential web vulnerabilities.")

            if not autocorrect:
                for finding in findings['results']:
                    click.echo(f"\n- Rule: {finding['check_id']}")
                    click.echo(f"  File: {finding['path']}:{finding['start']['line']}")
                    click.echo(f"  Message: {finding['extra']['message']}")
                return

            click.echo("[*] Starting AI-powered autocorrection for web vulnerabilities...")
            for finding in findings['results']:
                file_path = finding['path']
                start_line = finding['start']['line']
                end_line = finding['end']['line']
                rule_message = finding['extra']['message']
                
                with open(file_path, 'r') as f:
                    file_lines = f.readlines()

                vulnerable_snippet = "".join(file_lines[start_line - 1:end_line])
                
                file_extension = os.path.splitext(file_path)[1].lstrip('.')
                prompt = f"""
The following {file_extension} code from a web application has a vulnerability (Rule ID: {finding['check_id']}):
'{rule_message}'

Vulnerable code from '{file_path}':
```
{vulnerable_snippet}
```

Rewrite the vulnerable code snippet to fix the issue while maintaining its original functionality and style.
Return only the corrected code block, without any explanation or markdown formatting.
"""
                
                click.echo(f"\n[*] Analyzing vulnerability in {file_path}:{start_line}...")
                suggested_fix = call_ai_api(prompt).strip()

                if suggested_fix.startswith("```") and suggested_fix.endswith("```"):
                    suggested_fix = "\n".join(suggested_fix.split('\n')[1:-1])

                click.echo("[*] AI has suggested a fix. Please review the changes:")
                
                diff = difflib.unified_diff(
                    vulnerable_snippet.splitlines(keepends=True),
                    suggested_fix.splitlines(keepends=True),
                    fromfile='Original',
                    tofile='Patched',
                )
                
                for line in diff:
                    if line.startswith('+'):
                        click.secho(line, fg='green', nl=False)
                    elif line.startswith('-'):
                        click.secho(line, fg='red', nl=False)
                    else:
                        click.echo(line, nl=False)

                if click.confirm('\nDo you want to apply this patch?'):
                    new_file_lines = file_lines[:start_line - 1] + suggested_fix.splitlines(keepends=True) + file_lines[end_line:]
                    with open(file_path, 'w') as f:
                        f.writelines(new_file_lines)
                    click.echo(f"[*] Patch applied to {file_path}")
                    log_feedback(finding, suggested_fix, True)
                else:
                    click.echo("[*] Patch skipped.")
                    log_feedback(finding, suggested_fix, False)

        except FileNotFoundError:
            click.echo("Error: semgrep is not installed. Please install it to use this feature.", err=True)
        except json.JSONDecodeError:
            click.echo(f"Error parsing Semgrep JSON output.", err=True)
        except Exception as e:
            click.echo(f"An unexpected error occurred: {e}", err=True)
    asyncio.run(_web_async(path, autocorrect))


@cli.group()
def ai():
    """Commands for AI-powered analysis."""
    pass

@ai.command()
@click.option('--target', required=True, help='The target domain to analyze.')
def analyze(target):
    """Analyzes a target and its subdomains for potential vulnerabilities."""
    click.echo(f'[*] Starting AI analysis for {target}...')
    
    subdomain_list = find_subdomains(target)
    
    if subdomain_list is None:
        click.echo('[-] AI analysis aborted due to an error in subdomain enumeration.', err=True)
        return

    click.echo(f'[+] Found {len(subdomain_list)} subdomains. Preparing analysis...')
    
    prompt = f"Analyze the following domain and its subdomains for potential security vulnerabilities. Provide a brief summary of potential weak points and suggest attack vectors.\n\nDomain: {target}\n\nSubdomains: {', '.join(subdomain_list)}"
    
    analysis_result = call_ai_api(prompt)
    
    click.echo('\n--- AI Analysis ---')
    click.echo(analysis_result)
    click.echo('--- End of AI Analysis ---')

@ai.command('generate-payloads')
@click.option("--type", help="Payload type (e.g., xss, sqli, ssrf)", required=True)
@click.option("--target-tech", help="Target tech stack (e.g., php, nodejs)", default="")
def generate_payloads(type, target_tech):
    """Generate AI-powered attack payloads."""
    prompt = f"Generate 5 {type} payloads for {target_tech} applications. Return only a bulleted list."
    payloads = call_ai_api(prompt)
    click.echo(f"""Generated {type.upper()} payloads:
{payloads}""")

@ai.command('get-cve')
@click.argument('cve_id')
def get_cve(cve_id):
    """Fetches vulnerability data for a given CVE ID, utilizing caching."""
    click.echo(f"[*] Attempting to fetch data for {cve_id}...")
    data = get_vulnerability_data(cve_id)
    click.echo(json.dumps(data, indent=2))

@ai.command('generate-tests')
@click.argument('file_path', type=click.Path(exists=True))
def generate_tests(file_path):
    """Generates unit tests for a given code file using AI."""
    click.echo(f"[*] Generating tests for {file_path}...")

    try:
        with open(file_path, 'r') as f:
            code_content = f.read()
        
        file_extension = os.path.splitext(file_path)[1].lstrip('.')
        file_name = os.path.basename(file_path)

        prompt = f"""
Generate unit tests for the following {file_extension} code from the file '{file_name}'.
Focus on covering the main functionalities and edge cases.
Return only the test code block, without any explanation or markdown formatting.

Code:
```
{code_content}
```
"""
        
        generated_tests = call_ai_api(prompt).strip()

        if generated_tests.startswith("```") and generated_tests.endswith("```"):
            generated_tests = "\n".join(generated_tests.split('\n')[1:-1])

        test_file_name = f"test_{os.path.splitext(file_name)[0]}.py"
        test_file_path = os.path.join(os.path.dirname(file_path), test_file_name)

        click.echo("[*] AI has suggested tests. Please review them:")
        click.echo(generated_tests)

        if click.confirm(f'\nDo you want to save these tests to {test_file_path}?'):
            with open(test_file_path, 'w') as f:
                f.write(generated_tests)
            click.echo(f"[*] Tests saved to {test_file_path}")
        else:
            click.echo("[*] Test generation skipped.")

    except FileNotFoundError:
        click.echo(f"Error: File not found at {file_path}", err=True)
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}", err=True)


@cli.group()
def workflow():
    """Commands for managing and executing workflows."""
    pass

@workflow.command()
@click.argument('workflow_file', type=click.Path(exists=True))
def run(workflow_file):
    """Executes a defined workflow from a JSON or YAML file."""
    click.echo(f"[*] Running workflow from {workflow_file}...")
    log_audit_event("workflow_run", f"Workflow execution initiated for {workflow_file}", {"workflow_file": workflow_file})

    try:
        with open(workflow_file, 'r') as f:
            if workflow_file.endswith('.json'):
                workflow_definition = json.load(f)
            elif workflow_file.endswith('.yaml') or workflow_file.endswith('.yml'):
                workflow_definition = yaml.safe_load(f)
            else:
                click.echo("Error: Workflow file must be a .json, .yaml, or .yml file.", err=True)
                return

        if not isinstance(workflow_definition, list):
            click.echo("Error: Workflow definition must be a list of steps.", err=True)
            return

        final_context = execute_workflow(workflow_definition)
        click.echo("[*] Workflow execution complete. Final context:")
        click.echo(json.dumps(final_context, indent=2))

    except FileNotFoundError:
        click.echo(f"Error: Workflow file not found at {workflow_file}", err=True)
    except (json.JSONDecodeError, yaml.YAMLError) as e:
        click.echo(f"Error parsing workflow file: {e}", err=True)
    except Exception as e:
        click.echo(f"An unexpected error occurred during workflow execution: {e}", err=True)

@cli.group()
def vibe():
    """Commands for VibeOps engineering."""
    pass

@vibe.command()
@click.argument('prompt')
def interpret(prompt):
    """Interprets a natural language prompt and executes the corresponding command."""
    click.echo(f"[*] Interpreting your vibe: '{prompt}'...")
    
    # Create a context of available commands
    command_list = [
        "scan subdomains --target <domain>",
        "scan ports --target <domain> --top-ports <number>",
        "ai analyze --target <domain>",
        "ai generate-payloads --type <payload_type> --target-tech <technology>"
    ]
    
    # Ask the LLM to interpret the prompt
    llm_prompt = f"""
    Given the following user prompt, identify the command and its arguments from the list below.
    
    Available commands:
    - {', '.join(command_list)}
    
    User prompt: "{prompt}"
    
    Return the full command to execute. For example, if the prompt is "find subdomains for example.com", you should return "bughunter scan subdomains --target example.com".
    """
    
    command_to_run = call_ai_api(llm_prompt)
    
    if command_to_run.startswith("bughunter"):
        click.echo(f"[*] Executing: {command_to_run}")
        # Split the command to run it with subprocess
        command_parts = command_to_run.split()
        try:
            # We need to execute the bughunter command itself, so we assume it's in the path
            subprocess.run(command_parts, check=True)
        except subprocess.CalledProcessError as e:
            click.echo(f"Error executing command: {e}", err=True)
        except FileNotFoundError:
            click.echo("Error: 'bughunter' command not found. Make sure the package is installed correctly in your environment.", err=True)
    else:
        click.echo(f"Could not interpret the prompt into a valid command. AI response: {command_to_run}", err=True)

@cli.command()
def tags():
    """Displays the VibeOps engineering tags associated with this tool."""
    click.echo("--- VibeOps Engineering Tags ---")
    click.echo("- AI-Assisted Development")
    click.echo("- Developer Experience (DevEx)")
    click.echo("- Conversational Infrastructure (emerging)")
    click.echo("- CI/CD and Automation")
    click.echo("- AI SRE (AI Site Reliability Engineering)")
    click.echo("- Governance and Reliability")
    click.echo("---------------------------------")


cli.add_command(refactor)
cli.add_command(learn)
cli.add_command(pullpush_command)
cli.add_command(pullpush_command)
cli.add_command(pullpush_command)






if __name__ == '__main__':
    cli()
