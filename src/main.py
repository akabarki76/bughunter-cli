import click
import os
import shutil
import glob
import subprocess
import requests
import google.generativeai as genai
from github import Github
from dotenv import load_dotenv

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

def find_subdomains(target):
    """Finds subdomains of a target domain using crt.sh."""
    try:
        response = requests.get(f'https://crt.sh/?q=%.{target}&output=json')
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

def call_ai_api(prompt):
    """Calls the Gemini API and returns the response."""
    if not gemini_api_key:
        return "Error: GEMINI_API_KEY not configured. Please set it in your .env file."
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error calling Gemini API: {e}"

@click.group()
def cli():
    pass

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
    """Publishes the package to a specified repository (e.g., PyPI)."""
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
@click.option('--target', required=True, help='The target domain to scan for subdomains.')
def subdomains(target):
    """Finds subdomains of a target domain using crt.sh."""
    click.echo(f'[*] Searching for subdomains for {target}...')
    subdomain_list = find_subdomains(target)
    if subdomain_list:
        click.echo(f'[+] Found {len(subdomain_list)} unique subdomains:')
        for subdomain in subdomain_list:
            click.echo(subdomain)
    else:
        click.echo('[-] No subdomains found.')

@scan.command()
@click.argument("target")
@click.option("--top-ports", help="Scan top N ports (default: 100)", default=100)
def ports(target, top_ports):
    """Scan open ports on a target."""
    click.echo(f"[*] Scanning top {top_ports} ports on {target}...")
    if not shutil.which("nmap"):
        click.echo("Error: nmap is not installed. Please install it to use this feature.", err=True)
        return
    
    cmd = ["nmap", "--top-ports", str(top_ports), "-T4", target]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        click.echo(result.stdout)
    except FileNotFoundError:
        click.echo("Error: nmap is not installed. Please install it to use this feature.", err=True)
    except subprocess.CalledProcessError as e:
        click.echo(f"Error during nmap scan:\n{e.stderr}", err=True)


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
    click.echo(f"Generated {type.upper()} payloads:\n{payloads}")


if __name__ == '__main__':
    cli()