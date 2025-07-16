import click

@click.group()
def config():
    """Configuration for bughunter-cli."""
    pass

@config.command()
@click.argument('key')
@click.argument('value')
def set(key, value):
    """Sets a configuration key."""
    click.echo(f"Setting '{key}' to '{value}'...")
    click.echo("(This command is not yet implemented.)")
