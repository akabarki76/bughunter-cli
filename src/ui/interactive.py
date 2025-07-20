from rich.console import Console
from rich.table import Table

# Placeholder functions for showing fix suggestions and explanations
def show_fix_suggestion(vuln):
    """Placeholder for showing a fix suggestion."""
    print(f"Showing fix suggestion for {vuln['id']}")

def explain_mechanism(vuln):
    """Placeholder for explaining the vulnerability mechanism."""
    print(f"Explaining the mechanism for {vuln['id']}")

def explore_vulnerability(vuln):
    console = Console()
    
    while True:
        table = Table(title=f"Vulnerability: {vuln['id']}")
        table.add_column("Field")
        table.add_column("Value")
        
        for k, v in vuln.items():
            table.add_row(k, str(v))
            
        console.print(table)
        
        choice = console.input(
            "\n[b]Back[/b]  [f]Fix suggestion[/f]  [e]Explain[/e]  [q]Quit\n> "
        ).lower()
        
        if choice == "f":
            show_fix_suggestion(vuln)
        elif choice == "e":
            explain_mechanism(vuln)
        elif choice == "q":
            break

if __name__ == '__main__':
    # Example vulnerability object
    example_vuln = {
        "id": "CVE-2023-12345",
        "severity": "High",
        "description": "A critical SQL injection vulnerability.",
        "file": "/src/user_repository.py",
        "line": 42
    }
    explore_vulnerability(example_vuln)
