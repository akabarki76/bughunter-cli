import click
import requests
from src.utils.tool_registration import BaseTool, register_tool

def find_subdomains(target):
    """Finds subdomains of a target domain using crt.sh."""
    try:
        from urllib.parse import urlparse
        
        def validate_url(url):
            parsed = urlparse(url)
            if not parsed.scheme in ["http", "https"]:
                raise ValueError("Invalid URL scheme")
            return url

        url = f'https://crt.sh/?q=%.{target}&output=json'
        validate_url(url)
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes

        subdomains = set()
        for entry in response.json():
            name_value = entry.get('name_value', '')
            if name_value:
                # crt.sh returns multiple lines for some certs, split them
                for subdomain in name_value.split('\n'):
                    # Remove wildcard prefixes
                    if subdomain.startswith('*.'):
                        subdomain = subdomain[2:]
                    subdomains.add(subdomain.strip())
        return sorted(list(subdomains))

    except requests.exceptions.RequestException as e:
        click.echo(f'Error connecting to crt.sh: {e}', err=True)
        return None
    except ValueError:
        click.echo('Error parsing JSON response from crt.sh.', err=True)
        return None

@register_tool("subdomain_scanner")
class SubdomainScanner(BaseTool):
    """A tool to find subdomains of a target domain."""

    def execute(self, target, *args, **kwargs):
        """Finds subdomains of a target domain using crt.sh."""
        click.echo(f'[*] Searching for subdomains for {target}...')
        subdomain_list = find_subdomains(target)
        if subdomain_list:
            click.echo(f'[+] Found {len(subdomain_list)} unique subdomains:')
            for subdomain in subdomain_list:
                click.echo(subdomain)
        else:
            click.echo('[-] No subdomains found.')
