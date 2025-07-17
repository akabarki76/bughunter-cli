import click

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.syntax import Syntax
from src.utils.ai_utils import call_ai_api

console = Console()

@click.group()
def learn():
    """Interactive vulnerability learning modules."""
    pass

@learn.command('explain-vuln')
@click.argument('vulnerability_summary')
@click.option('--code-snippet', help='An optional code snippet related to the vulnerability.')
def explain_vuln(vulnerability_summary, code_snippet):
    """Explains a vulnerability interactively using AI and Rich display."""
    click.echo(f"[*] Fetching explanation for: {vulnerability_summary}...")

    ai_prompt = f"""
Provide a detailed explanation for the following security vulnerability: '{vulnerability_summary}'.

If a code snippet is provided, analyze it in the context of this vulnerability and explain how the vulnerability manifests in that code.

Code snippet (if available):
```
{code_snippet if code_snippet else "No code snippet provided."}
```

Structure your response clearly, explaining:
1. What the vulnerability is.
2. How it works.
3. Potential impact.
4. How to mitigate it.

Return the explanation in a clear, readable format, suitable for a console display. Do not include markdown code blocks for the explanation itself, only for the provided code snippet if you choose to re-display it.
"""

    explanation_text = call_ai_api(ai_prompt)

    with Live(console=console, screen=True, auto_refresh=True, vertical_overflow="visible") as live:
        live.update(Panel(f"[bold blue]Vulnerability Explanation: {vulnerability_summary}[/bold blue]\n\n{explanation_text}", border_style="green"))
        
        if code_snippet:
            syntax = Syntax(code_snippet, "python", theme="monokai", line_numbers=True)
            live.update(Panel(syntax, title="[bold yellow]Provided Code Snippet[/bold yellow]", border_style="yellow"))

        console.input("[bold cyan]Press Enter to continue...[/bold cyan]")

    click.echo("[*] Interactive explanation finished.")