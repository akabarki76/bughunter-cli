import sys
import os
from click.testing import CliRunner

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.main import cli

def test_hello_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['hello', '--name', 'TestUser'])
    assert result.exit_code == 0
    assert 'Hello, TestUser!' in result.output

def test_hello_command_default():
    runner = CliRunner()
    result = runner.invoke(cli, ['hello'])
    assert result.exit_code == 0
    assert 'Hello, World!' in result.output
