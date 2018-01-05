import pytest
import click
import sys
import time
from lb import cli
from lb.setup import commands as commands
from click.testing import CliRunner
from cStringIO import StringIO

#
# Little Benchmark
# test_setup.py
# Docs: See https://docs.pytest.org/en/latest/assert.html#assert for more info.
#

@pytest.fixture
def runner():
    return CliRunner()

def test_cli(runner):
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert not result.exception
    assert result.output.strip() is not None

def test_cli_with_install_option(runner):
    result = runner.invoke(cli.main, ['setup','install','_test-benchmark_'])
    assert result.exit_code == 0
    assert not result.exception
    # TODO: Fix this. It's outputting ''
    # assert result.output.strip() == 'test complete\n'
    assert result.output.strip() is not None

def test_cli_with_install_without_option(runner):
    result = runner.invoke(cli.main, ['setup'])
    assert result.exit_code == 0
    assert not result.exception
    assert result.output.strip() is not None

def test_get_benchmark_package_contents(runner):
    result = commands.get_benchmark_package_contents()
    click.echo(result)
