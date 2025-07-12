import click
import os
import shutil
import glob
import subprocess
from github import Github

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
    click.echo(f'Attempting to create PR in {repo}...')
    click.echo(f'  Title: {title}')
    click.echo(f'  Head: {head}')
    click.echo(f'  Base: {base}')
    click.echo(' (This is a placeholder for actual GitHub API call to create PR.)')

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

@cli.command()
@click.option('--repository', default='pypi', help='The repository to publish to (e.g., pypi, testpypi).')
def publish(repository):
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

if __name__ == '__main__':
    cli()

