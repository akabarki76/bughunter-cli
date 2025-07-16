import click

@click.command()
@click.option('--output', required=True, type=click.Path(), help='Output file path for the vulnerability map.')
def map(output):
    """Visual vulnerability mapping."""
    click.echo(f"Generating vulnerability map to '{output}'...")
    click.echo("(This command is not yet implemented.)")
