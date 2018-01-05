import pytest
import click
from click.testing import CliRunner
from lb import cli
from lb.system import commands

#
# Little Benchmark
# test_system.py
# Docs: See https://docs.pytest.org/en/latest/assert.html#assert for more info.
#

@pytest.fixture
def runner():
    return CliRunner(echo_stdin=True)

def test_cli(runner):
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert not result.exception
    assert result.output.strip() is not None

def test_cli_with_config_option(runner):
    result = runner.invoke(cli.main, ['system','config'])
    assert not result.exception
    assert result.exit_code == 0
    assert result.output.strip() is not None

def test_cli_with_info_option(runner):
    result = runner.invoke(cli.main, ['system','info'])
    assert not result.exception
    assert result.exit_code == 0
    assert result.output.strip() is not None

def test_cli_get_sys_name_valid(runner):
    result = commands.get_sys_name('linux2')
    assert result is not None
    assert result == 'Linux'

def test_cli_get_sys_name_invalid(runner):
    with pytest.raises(NameError) as exc_info:
        commands.get_sys_name(linux2)
    assert "global name 'linux2' is not defined" in str(exc_info.value)
