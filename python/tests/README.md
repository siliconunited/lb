# Testing

This Python project uses `pytest` as the testing framework (See [#Framework](#framework) below) and `tox` to help automate it all.

Run the following to launch tests: `$ tox`

> tox is an automation tool providing packaging, testing and deployment of Python software right from the console or CI server.

# Framework

If you don't already have `pytest` installed. Install it with `pip install pytest` and if you have issues [see pytest installation documentation](http://doc.pytest.org/en/latest/getting-started.html#installation). Afterwards, run `pytest` to launch the tests.

To learn more about the testing platform, read about [pytest](http://doc.pytest.org/en/latest/contents.html#toc).

`pytest` will run all files in the `tests/` directory and its subdirectories with the form `test_*.py` or `*_test.py`. More generally, it follows [standard test discovery rules](http://doc.pytest.org/en/latest/goodpractices.html#test-discovery).

Run quietly with `pytest -q tests`

# Coverage

For coverage reports, install `pytest-cov`.
