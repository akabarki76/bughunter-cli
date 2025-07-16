import pytest
from src.utils.security import validate_url

def test_valid_urls():
    assert validate_url("https://example.com") == "https://example.com"
    assert validate_url("http://sub.domain.co.uk/path") == "http://sub.domain.co.uk/path"

def test_invalid_urls():
    with pytest.raises(ValueError):
        validate_url("javascript:alert(1)")
        
    with pytest.raises(ValueError):
        validate_url("ftp://unsecure-server")
        
    with pytest.raises(ValueError):
        validate_url("http://")
