import click
import os

from lb.helpers.config import pass_config

"""

HELPER FUNCTIONS

"""

"""

END HELPER FUNCTIONS

"""


"""

CLICK COMMANDS

"""

"""
system

Initialization method

Notes:
- When setting up options, the order matters. So for instance if benchmark directory
is the fourth item in the list. It should come fourth in function e.g., system(.., .., .., benchmark_directory, ..)
- Options that contain a dash (-) will need to be passed as variables with underscores (_) e.g., --benchmark-directory becomes benchmark_directory
"""
@click.group()
@pass_config
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode.')
@click.option('-d', '--debug', is_flag=True, help='Enables debug mode.')
@click.option('--benchmark-directory', default='benchmarks', type=click.Path(), help='Sets the path to the benchmark directory.')
@click.option('--log-directory', default='logs', type=click.Path(), help='Sets the path for the logs.')
@click.option('--log-file', default='debug.log', help='Sets the name of log file.')
@click.option('--install-path', default='.littlebenchmark', help='Sets the install path for the benchmark dependencies.')
@click.option('--install-file', default='install.sh', help='Sets the benchmark install shell command to run.')
@click.option('--definition-file', default='test-definition.json', help='Sets the test definition file to use.')
@click.option('--result-definition-file', default='results-definition.json', help='Sets the results definition file to use.')
@click.option('--downloads-file', default='downloads.json', help='Sets the file containing benchmark download information.')
@click.option('--temporary-directory', default='.littlebenchmark', type=click.Path(), help='Sets the path to the temporary directory.')
@click.version_option()
def system(config, verbose, debug, benchmark_directory, log_directory, log_file, install_path, install_file, definition_file, result_definition_file,  downloads_file, temporary_directory):
    config.verbose = verbose
    config.debug = debug
    if benchmark_directory:
        config.benchmark_directory = benchmark_directory
    if log_directory:
        config.log_directory = log_directory
    if log_file:
        config.log_file = log_file
    if install_path:
        config.install_path = os.path.abspath(install_path)
    if install_file:
        config.install_file = install_file
    if definition_file:
        config.definition_file = definition_file
    if result_definition_file:
        config.result_definition_file = result_definition_file
    if downloads_file:
        config.downloads_file = downloads_file
    if temporary_directory:
        config.temporary_directory = os.path.abspath(temporary_directory)

# config
# Handles printing out the config variables that are set.
@system.command()
@pass_config
def config(config):
    """Shows the current config settings"""
    click.echo('-------------- Context Config ---------------')
    click.echo('debug: ' + str(config.debug))
    click.echo('version: ' + str(config.version))
    click.echo('codename: ' + str(config.codename))
    click.echo('verbose: ' + str(config.verbose))
    click.echo('temporary-directory: ' + config.temporary_directory)
    click.echo('benchmark-directory: ' + config.benchmark_directory)
    click.echo('package-directory: ' + config.package_directory)
    click.echo('log-directory: ' + config.log_directory)
    click.echo('log-file: ' + config.log_file)
    click.echo('install-file: ' + config.install_file)
    click.echo('downloads-file: ' + config.downloads_file)
    click.echo('default-package-file: ' + config.default_package_file)
    click.echo('---------------------------------------------')
    click.echo(nl=True)
    click.echo('-------------- System Details ---------------')
    click.echo('ssl-version: ' + str(config.ssl_version))
    click.echo('system: ' + str(config.sys))
    click.echo('system-name: ' + str(config.sysname))
    click.echo('os-name: ' + str(config.osname))
    click.echo('cpus: ' + str(config.cpu_count))
    # The tuple contains 5 strings: (sysname, nodename, release, version, machine).
    click.echo('system-info: ')
    for data in config.uname:
        click.echo('  ' + str(data))
    click.echo('---------------------------------------------')
    click.echo(nl=True)

# info
# Handles printing out info about the CLI
@system.command()
@pass_config
def info(config):
    """More info about the CLI."""
    click.echo(click.style(' Little Benchmark Test Suite v' + str(config.version) + ' (' + config.codename + ') ', bg='black', fg='magenta', bold=True))
    click.echo(nl=True)
    click.echo('The',nl=False)
    click.echo(click.style(' Little Benchmark Suite ',bold="True"),nl=False)
    click.echo('is the most comprehensive Python testing and benchmarking platform available for Linux and OS X operating systems. The suite allows for carrying out tests in a fully automated manner from test installation to execution and reporting. All tests are meant to be easily reproducible, easy-to-use, and support fully automated execution. This toolset is protected under a commercial license and is developed by Silicon United.')
    click.echo(nl=True)
    click.echo('View the included PDF / HTML documentation or visit ' + config.url1 + ' for full details.')

@click.command()
def tools():
    click.echo(nl=True)
    """TEST INSTALLATION"""
    click.echo('TEST INSTALLATION')
    click.echo('\tinstall\t\t\t\t\t[Test | Suite | SiliconUnited ID | Test Result]  ...')
    # click.echo('\tinstall-dependencies\t\t\t[Test | Suite | SiliconUnited ID | Test Result]  ...')
    # click.echo('\tmake-download-cache')
    # click.echo('\tremove-installed-test\t\t\t[Test]')
    click.echo(nl=True)

    click.echo(nl=True)
    """TESTING"""
    click.echo('TESTING')
    # click.echo('\tauto-compare')
    click.echo('\tbenchmark\t\t\t\t[Test | Suite | SiliconUnited ID | Test Result]  ...')
    # click.echo('\tfinish-run\t\t\t\t[Test Result]')
    click.echo('\trun\t\t\t\t\t[Test | Suite | SiliconUnited ID | Test Result]  ...')
    click.echo('\trun-random-tests')
    # click.echo('\trun-tests-in-suite')
    # click.echo('\tstress-run \t\t\t\t[Test | Suite | SiliconUnited ID | Test Result]  ...')
    click.echo(nl=True)

    # click.echo(nl=True)
    # """BATCH TESTING"""
    # click.echo('BATCH TESTING')
    # click.echo('\tauto-compare')
    # click.echo('\tbenchmark\t\t\t\t[Test | Suite | SiliconUnited ID | Test Result]  ...')
    # click.echo('\tfinish-run\t\t\t\t[Test Result]')
    # click.echo('\trun\t\t\t\t\t[Test | Suite | SiliconUnited ID | Test Result]  ...')
    # click.echo('\trun-random-tests')
    # click.echo('\trun-tests-in-suite')
    # click.echo('\tstress-run\t\t\t\t[Test | Suite | SiliconUnited ID | Test Result]  ...')
    # click.echo(nl=True)

    # click.echo(nl=True)
    # """SILICONUNITED.COM"""
    # click.echo('SILICONUNITED.COM')
    # click.echo('\tclone-result\t\t\t\t[SiliconUnited ID]  ...')
    # click.echo('\tlist-recommended-tests')
    # click.echo('\tmake-su-cache')
    # click.echo('\tsu-changes')
    # click.echo('\tsu-launcher')
    # click.echo('\tsu-login')
    # click.echo('\tsu-refresh')
    # click.echo('\tsu-repositories')
    # click.echo('\tupload-result\t\t\t\t[Test Result]')
    # click.echo('\tupload-test-profile')
    # click.echo('\tupload-test-suite')
    # click.echo(nl=True)

    # click.echo(nl=True)
    # """SYSTEM"""
    # click.echo('SYSTEM')
    # click.echo('\tdiagnostics')
    # click.echo('\tsystem-info')
    # click.echo('\tsystem-sensors')
    # click.echo(nl=True)

    # click.echo(nl=True)
    # """INFORMATION"""
    # click.echo('INFORMATION')
    # click.echo('\testimate-run-time\t\t\t[Test | Suite | SiliconUnited ID | Test Result]')
    # click.echo('\tinfo\t\t\t\t\t[Test | Suite | SiliconUnited ID | Test Result]')
    # click.echo('\tlist-available-suites')
    # click.echo('\tlist-available-tests')
    # click.echo('\tlist-available-virtual-suites')
    # click.echo('\tlist-installed-dependencies')
    # click.echo('\tlist-installed-suites')
    # click.echo('\tlist-installed-tests')
    # click.echo('\tlist-missing-dependencies')
    # click.echo('\tlist-not-installed-tests')
    # click.echo('\tlist-possible-dependencies')
    # click.echo('\tlist-saved-results')
    # click.echo('\tlist-test-usage')
    # click.echo('\tlist-unsupported-tests')
    # click.echo(nl=True)

    # click.echo(nl=True)
    # """ASSET CREATION"""
    # click.echo('ASSET CREATION')
    # click.echo('\tdebug-benchmark\t\t\t\t[Test | Suite | SiliconUnited ID | Test Result]  ...')
    # click.echo('\tdebug-install\t\t\t\t[Test | Suite | SiliconUnited ID | Test Result]  ...')
    # click.echo('\tdebug-result-parser\t\t\t[Test | Suite | SiliconUnited ID | Test Result]  ...')
    # click.echo('\tdebug-test-download-links\t\t[Test | Suite | SiliconUnited ID | Test Result]')
    # click.echo('\tdownload-test-files\t\t\t[Test | Suite | SiliconUnited ID | Test Result]  ...')
    # click.echo('\tforce-install\t\t\t\t[Test | Suite | SiliconUnited ID | Test Result]  ...')
    # click.echo('\tresult-file-to-suite\t\t\t[Test Result]')
    # click.echo('\tvalidate-result-file')
    # click.echo('\tvalidate-test-profile')
    # click.echo('\tvalidate-test-suite')
    # click.echo(nl=True)

    # click.echo(nl=True)
    # """RESULT MANAGEMENT"""
    # click.echo('RESULT MANAGEMENT')
    # click.echo(nl=True)
    # click.echo('\tauto-sort-result-file\t\t\t[Test Result]')
    # click.echo('\tedit-result-file\t\t\t[Test Result]')
    # click.echo('\textract-from-result-file\t\t[Test Result]')
    # click.echo('\tmerge-results\t\t\t\t[Test Result]  ...')
    # click.echo('\trefresh-graphs\t\t\t\t[Test Result]')
    # click.echo('\tremove-from-result-file\t\t\t[Test Result]')
    # click.echo('\tremove-result\t\t\t\t[Test Result]')
    # click.echo('\trename-identifier-in-result-file\t[Test Result]')
    # click.echo('\trename-result-file\t\t\t[Test Result]')
    # click.echo('\treorder-result-file\t\t\t[Test Result]')
    # click.echo('\tresult-file-to-csv\t\t\t[Test Result]')
    # click.echo('\tresult-file-to-json\t\t\t[Test Result]')
    # click.echo('\tresult-file-to-pdf\t\t\t[Test Result]')
    # click.echo('\tresult-file-to-text\t\t\t[Test Result]')
    # click.echo('\tshow-result\t\t\t\t[Test Result]')
    # click.echo('\twinners-and-losers\t\t\t[Test Result]')

    # click.echo(nl=True)
    # """RESULT ANALYTICS"""
    # click.echo('RESULT ANALYTICS')
    # click.echo(nl=True)
    # click.echo('\tanalyze-all-runs [Test Result]')

    # click.echo(nl=True)
    # """OTHER"""
    # click.echo('OTHER')
    # click.echo(nl=True)
    # click.echo('\tbuild-suite')
    # click.echo('\tdebug-dependency-handler')
    # click.echo('\tdebug-render-test')
    # click.echo('\tdebug-self-test')
    # click.echo('\tenterprise-setup')
    # click.echo('\thelp')
    # click.echo('\tnetwork-setup')
    # click.echo('\tuser-config-reset')
    # click.echo('\tuser-config-set')
    # click.echo('\tversion')

    # click.echo(nl=True)
    # """WEB / GUI SUPPORT"""
    # click.echo('WEB / GUI SUPPORT')
    # click.echo(nl=True)
    # click.echo('\tgui')
    # click.echo('\tstart-remote-gui-server')
    # click.echo('\tstart-lb-server')

    # click.echo(nl=True)
    # """MODULES"""
    # click.echo('MODULES')
    # click.echo(nl=True)
    # click.echo('\tlist-modules')

    # click.echo(nl=True)
    # """SERVER"""
    # click.echo('SERVER')
    # click.echo(nl=True)
    # click.echo('\tstart-server')
    # click.echo(nl=True)
"""

END CLICK COMMANDS

"""
