from src.utils.tool_registration import BaseTool, register_tool
import click
import json
from src.utils.policy_manager import load_security_policy

@register_tool("config")
class ConfigTool(BaseTool):
    name = "config"
    description = "Configuration for bughunter-cli."

    def run(self, key=None, value=None, view=False, **kwargs):
        """Handles configuration settings for bughunter-cli."""
        if view:
            policy = load_security_policy()
            click.echo("[*] Current Security Policy:")
            click.echo(json.dumps(policy, indent=2))
        elif key and value:
            click.echo(f"Setting '{key}' to '{value}'...")
            click.echo("(This command is not yet implemented.)")
        else:
            click.echo("Usage: bughunter run config --view or bughunter run config --key <key> --value <value>")
