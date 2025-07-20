import click
import subprocess
from src.utils.tool_registration import BaseTool, register_tool

@register_tool("port_scanner")
class PortScanner(BaseTool):
    """A tool to scan for open ports on a target."""
    dependencies = ["nmap"]

    def execute(self, target, top_ports=100):
        """Scan open ports on a target."""
        click.echo(f"[*] Scanning top {top_ports} ports on {target}...")
        
        cmd = ["nmap", "--top-ports", str(top_ports), "-T4", target]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            click.echo(result.stdout)
        except FileNotFoundError:
            # This check is redundant due to the dependency check in the base class,
            # but it's good practice to keep it for clarity.
            click.echo("Error: nmap is not installed. Please install it to use this feature.", err=True)
        except subprocess.CalledProcessError as e:
            click.echo(f"Error during nmap scan:\n{e.stderr}", err=True)

