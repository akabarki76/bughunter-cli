# Unified output formatter (src/utils/formatters.py)
def format_output(tool_name, output):
    if tool_name == "nmap":
        return _parse_nmap(output)
    elif tool_name == "dirsearch":
        return _parse_dirsearch(output)
    # ... other parsers
    return None
def _parse_nmap(data):
    # Extract open ports and services
    return {
        "ports": [],
        "services": [],
        "vulnerabilities": []
    }

def _parse_dirsearch(data):
    # Extract found directories
    return {
        "directories": []
    }
