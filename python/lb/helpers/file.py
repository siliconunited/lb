# file.py
# Contains helper functions related to manipulating files or directories

import click
import os

# Handles removing a file from the system
def remove_file(path, fn):
    try:
        click.echo('Removed existing file ' + os.path.join(path, fn))
        os.remove(os.path.join(path, fn))
    except OSError:
        click.echo('Unable to remove the file ' + os.path.join(path, fn))

# Handles removing a directory from the system
def remove_directory(top_dir):
    try:
        click.echo('Removed existing directory ' + top_dir)
        for root, dirs, files in os.walk(top_dir, topdown=False):
            for name in files:
                click.echo('Removed file ' + os.path.join(root, name))
                os.remove(os.path.join(root, name))
            for name in dirs:
                click.echo('Removed directory ' + os.path.join(root, name))
                os.rmdir(os.path.join(root, name))
    except OSError:
        click.echo('Unable to remove the directory ' + top_dir)
