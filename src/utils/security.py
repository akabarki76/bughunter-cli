from urllib.parse import urlparse
from functools import wraps

def validate_url(url):
    """Strict URL validation with scheme verification"""
    parsed = urlparse(url)
    if not parsed.scheme or parsed.scheme not in ["http", "https"]:
        raise ValueError(f"Invalid URL scheme: {url}")
    if not parsed.netloc:
        raise ValueError(f"Missing domain in URL: {url}")
    return url

def sanitized_url(func):
    """Decorator for URL sanitization"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'url' in kwargs:
            kwargs['url'] = validate_url(kwargs['url'])
        return func(*args, **kwargs)
    return wrapper
