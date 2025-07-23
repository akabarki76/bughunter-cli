

import pytest
from urllib.parse import urlparse
from src.main import analyze

from unittest.mock import patch

from click.testing import CliRunner
from src.main import analyze
from unittest.mock import patch, MagicMock





@patch('src.main.call_ai_api')
@patch('src.main.find_subdomains')
def test_ai_analyze(mock_find_subdomains, mock_call_ai_api):
    # Mock the functions that have external dependencies
    mock_find_subdomains.return_value = ['blog.example.com', 'api.example.com']
    mock_call_ai_api.return_value = "Critical: SQLi in /login.php"

    runner = CliRunner()
    result = runner.invoke(analyze, ['--target', 'example.com'])

    assert result.exit_code == 0
    assert "Starting AI analysis for example.com" in result.output
    assert "Found 2 subdomains" in result.output
    assert "Critical: SQLi in /login.php" in result.output
    
    # Verify that the mocks were called correctly
    mock_find_subdomains.assert_called_once_with('example.com')
    mock_call_ai_api.assert_called_once()
    # You could also add more specific assertions on the prompt passed to the AI
    prompt_arg = mock_call_ai_api.call_args[0][0]


    # Substring checks removed; see validation below.


    # Extract subdomains from the prompt_arg and validate them
    # This assumes the prompt_arg contains the subdomains as part of a URL or directly.
    # For this test, we'll check if the subdomains are present in the prompt_arg
    # and then validate them as if they were part of a URL.
    
    # In a real scenario, you'd use a more robust regex or NLP to extract URLs from the prompt.
    # For the purpose of this test, we'll assume the subdomains are directly present.
    
    # Extract hostnames from the prompt_arg using regex and validate them
    import re
    hostname_pattern = r'\b([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b'
    found_blog = False
    found_api = False
    for match in re.findall(hostname_pattern, prompt_arg):
        if is_valid_subdomain(match, "blog.example.com"):
            found_blog = True
        if is_valid_subdomain(match, "api.example.com"):
            found_api = True

    assert found_blog, "blog.example.com not found or invalid in prompt_arg"
    assert found_api, "api.example.com not found or invalid in prompt_arg"

    from urllib.parse import urlparse
    parsed_prompt = urlparse(prompt_arg)
    assert parsed_prompt.hostname and is_valid_subdomain(parsed_prompt.hostname, "blog.example.com")
    assert parsed_prompt.hostname and is_valid_subdomain(parsed_prompt.hostname, "api.example.com")

