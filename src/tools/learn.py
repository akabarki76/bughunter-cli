import click

@click.command()
@click.argument('vulnerability_name')
def learn(vulnerability_name):
    """Interactive vulnerability learning modules."""
    click.echo(f"Loading learning module for '{vulnerability_name}'...")
    click.echo("(This command is not yet implemented.)")
