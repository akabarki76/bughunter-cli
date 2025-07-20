import click
from ..utils.shell import run_shell_command

@click.command()
@click.option('--branch', default='main', help='The branch to pull from and push to.')
def pullpush(branch):
    """A command to pull and push changes to a git repository."""
    click.echo(f"Pulling changes from {branch}...")
    pull_result = run_shell_command(f"git pull origin {branch}")
    if pull_result["returncode"] != 0:
        click.echo("Error pulling changes:")
        click.echo(pull_result["stderr"])
        return

    click.echo("Pushing changes...")
    push_result = run_shell_command(f"git push origin {branch}")
    if push_result["returncode"] != 0:
        click.echo("Error pushing changes:")
        click.echo(push_result["stderr"])
        return

    click.echo("Pull and push successful!")
