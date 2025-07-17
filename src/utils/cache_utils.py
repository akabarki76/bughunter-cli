from cachetools import cached, TTLCache

# Define a cache for vulnerability data with a TTL of 1 hour (3600 seconds)
# and a maximum of 1000 entries.
vulnerability_cache = TTLCache(maxsize=1000, ttl=3600)

@cached(vulnerability_cache)
def get_vulnerability_data(cve_id: str) -> dict:
    """
    Placeholder function to simulate fetching vulnerability data by CVE ID.
    In a real scenario, this would fetch data from a vulnerability database.
    """
    print(f"[*] Fetching vulnerability data for CVE: {cve_id} (this would be from an external source)")
    # Simulate a network request or database lookup
    return {"cve_id": cve_id, "description": f"Details for {cve_id}", "severity": "High"}
