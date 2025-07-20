from click.testing import CliRunner
from src.main import analyze
from unittest.mock import patch, MagicMock
import pytest
from urllib.parse import urlparse



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
    
    assert "blog.example.com" in prompt_arg
    assert "api.example.com" in prompt_arg
