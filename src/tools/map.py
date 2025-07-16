from src.tool_manager import Plugin, register_plugin
import click

@register_plugin("map")
class Map(Plugin):
    """Visual vulnerability mapping."""
    def execute(self, output, **kwargs):
        """Visual vulnerability mapping."""
        click.echo(f"Generating vulnerability map to '{output}'...")
        click.echo("(This command is not yet implemented.)")
