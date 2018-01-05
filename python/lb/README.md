# The Little Benchmark CLI
> You found Little Benchmark's heart. This folder contains a majority of the code responsible for running and controlling the various commands of the CLI.

# Installation
If you don't use [`pipsi`](https://github.com/mitsuhiko/pipsi), you're missing out.
Here are [installation instructions](https://github.com/mitsuhiko/pipsi#readme).

## Locally

To install the script locally for testing and development run the following command: `$ pipsi install --editable . `

Afterwards, run the following to see if the script installed: `$ lb ` or `$ lb --help `

## Remote Deployment

When the user downloads the script and is ready to install, they will use the following command:
```
$ pipsi install ../path/to/project/dir   # install locally
```

> Note: Make sure you've activated `virtualenv` before running the `pipsi` command.**

To uninstall the script locally run: `$ pipsi uninstall .`

# Testing

You can find more by navigating to the [tests](/tests/) folder and checking out the [README](/tests/README.md).

# Documentation

You can find more by navigating to the [docs](/docs/) folder and checking out the [README](/docs/README.md).

# Standards

For style guide enforcement, [Flake8](http://flake8.pycqa.org/en/latest/) is being used. Install with `pip install flake8`

# Dependencies
The following dependencies can be installed using the following command:
`pip install *****`

- [click](http://click.pocoo.org/5/) - Click is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary.
- [pipsi](https://github.com/mitsuhiko/pipsi#readme) - pip script installer

## Continuous Integration

See the [README](/ci/README.md) in the [ci](/ci/) folder for more.

# Virtualenv

If you've run the `install.sh` shell script, the following should already be set up for you.

If you're not aware of the benefits of such, [read this](https://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/). Install `virtualenv` with `$ pip install virtualenv`. Also have a look at the [click documentation](http://click.pocoo.org/5/quickstart/#virtualenv) regarding virtualenv.

```
$ virtualenv env
```

Activate the environment so you don't have to keep typing `env/bin/YOUR_COMMAND`.
```
$ . env/bin/activate
```

Windows users would use the following:
```
$ venv\scripts\activate
```

Deactivate virtualenv via:
```
$ deactivate
```

## Setuptools Integration

This has already been setup in the project, but [Setuptools integration](http://click.pocoo.org/5/setuptools/#setuptools-integration) is probably worth getting familiar with.

# Resources
- [tox](https://tox.readthedocs.io/en/latest/) - Tox is a generic virtualenv management and test command line tool
- [cookiecutter](http://cookiecutter.readthedocs.io/en/latest/)
- [Writing a Command-Line Tool in Python](http://nvie.com/posts/writing-a-cli-in-python-in-under-60-seconds/)
- [Testing Click Applications](http://click.pocoo.org/5/testing/)
- [Click Test Example:test_testing.py](https://github.com/pallets/click/blob/master/tests/test_testing.py)
- [Click Examples](https://github.com/pallets/click/tree/master/examples)
- [python-pts-openbenchmarking](https://github.com/davidovitch/python-pts-openbenchmarking/)
- [How can I split my Click commands, each with a set of sub-commands, into multiple files?](http://stackoverflow.com/questions/34643620/how-can-i-split-my-click-commands-each-with-a-set-of-sub-commands-into-multipl)
- ~~[How to Set Up TravisCI-like Continuous Integration with Docker and Jenkins](https://zapier.com/engineering/continuous-integration-jenkins-docker-github/)~~
- ~~[Docker Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Docker+Plugin)~~
- [Simplify Your Life With an SSH Config File](http://nerderati.com/2011/03/17/simplify-your-life-with-an-ssh-config-file/)
- [How can I install a private module with public dependencies in pip?](http://stackoverflow.com/questions/14288313/how-can-i-install-a-private-module-with-public-dependencies-in-pip)

# Videos Tutorials
- [Building Command Line Applications with Click](https://www.youtube.com/watch?v=kNke39OZ2k0)
