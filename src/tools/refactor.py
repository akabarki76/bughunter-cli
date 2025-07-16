import click
import os
import difflib
from src.utils.ai_utils import call_ai_api
from src.utils.security import log_audit_event

@click.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--prompt', required=True, help='A description of the desired refactoring.')
def refactor(file_path, prompt):
    """AI-assisted code refactoring."""
    click.echo(f"[*] Starting AI-assisted refactoring for {file_path}...")
    log_audit_event("refactor_code", f"AI-assisted refactoring initiated for {file_path}", {"file_path": file_path, "prompt": prompt})

    try:
        with open(file_path, 'r') as f:
            original_code = f.read()
        
        file_extension = os.path.splitext(file_path)[1].lstrip('.')
        file_name = os.path.basename(file_path)

        ai_prompt = f"""
Refactor the following {file_extension} code from the file '{file_name}' based on the following instructions:
'{prompt}'

Original code:
```
{original_code}
```

Return only the refactored code block, without any explanation or markdown formatting.
"""
        
        suggested_refactoring = call_ai_api(ai_prompt).strip()

        if suggested_refactoring.startswith("```") and suggested_refactoring.endswith("```"):
            suggested_refactoring = "\n".join(suggested_refactoring.split('\n')[1:-1])

        click.echo("[*] AI has suggested a refactoring. Please review the changes:")
        
        diff = difflib.unified_diff(
            original_code.splitlines(keepends=True),
            suggested_refactoring.splitlines(keepends=True),
            fromfile='Original',
            tofile='Refactored',
        )
        
        for line in diff:
            if line.startswith('+'):
                click.secho(line, fg='green', nl=False)
            elif line.startswith('-'):
                click.secho(line, fg='red', nl=False)
            else:
                click.echo(line, nl=False)

        if click.confirm('\nDo you want to apply this refactoring?'):
            with open(file_path, 'w') as f:
                f.write(suggested_refactoring)
            click.echo(f"[*] Refactoring applied to {file_path}")
        else:
            click.echo("[*] Refactoring skipped.")

    except FileNotFoundError:
        click.echo(f"Error: File not found at {file_path}", err=True)
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}", err=True)
