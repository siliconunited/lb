import click

from lb.system import commands as system
from lb.setup import commands as setup
# from .tools import commands as tools

"""

HELPER FUNCTIONS

"""

"""

END HELPER FUNCTIONS

"""

@click.group()
def main():
    """Little Benchmark Test Suite"""
    pass

# Add the commands from the other files via their group
main.add_command(setup.setup)
main.add_command(system.system)
