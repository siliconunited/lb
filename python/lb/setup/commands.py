import click
import os
import platform
import json
import progressbar
from subprocess import call

from lb.classes.curl import CURLDownloadFileList

from lb.helpers.config import pass_config
from lb.helpers import file as file_helpers

"""

HELPER FUNCTIONS

"""

# make_required_folders
# Handles making the required folders for the benchmark suite
def make_required_folders(install_path, temporary_directory):
    click.echo('Making the required folders...')
    # Make the install path if it does not exists
    if not os.path.exists(install_path):
        os.makedirs(install_path)

    # Make the temporary directory path if it does not exists
    if not os.path.exists(temporary_directory):
        os.makedirs(temporary_directory)

# download_benchmarks
# Handles downloading items from a json file
def download_benchmarks(benchmark_array):
    # Holds the benchmark details
    content = {}
    definitions = {}

    # Traverse through the benchmark array.
    # The names should correspond to a folder in the set benchmark directory.
    for item in benchmark_array:

        # Parse the downloads file
        content[item] = parse_downloads_file(
                config.benchmark_directory,
                config.downloads_file,
                config.temporary_directory,
                item
            )

        # Parse the test definition file and search for other dependencies
        definitions[item] = parse_test_definition_file(
                config.benchmark_directory,
                item,
                config.definition_file
            )

        # The dependencies should be in the following attribute if they exist
        # definitions[item]['dependencies']
        # TODO: Get them out and download them from API or maybe they're already local like the rest.

    # Process the downloads
    download_file(content)
    download_file(definitions)

# download_file
# Handles the actual downloading of the file.
def download_file(content):
    # Create the download request
    c = CURLDownloadFileList()
    c.start(content, config.log_directory)

# parse_test_definition_info
# Handles parsing the info section of the test definition file
def parse_test_definition_info(data):
    return {
            'title': str(data['Title']),
            'version': str(data['Version']),
            'description': str(data['Description']),
            'sub_title': str(data['SubTitle'])
        }

# parse_test_definition_profile
# Handles parsing the profile section of the test definition file
def parse_test_definition_profile(data):
    return {
            'version': str(data['Version']),
            'supported_platforms': str(data['SupportedPlatforms']),
            'software_type': str(data['SoftwareType']),
            'dependencies': str(data['Dependencies']),
            'external_depends': str(data['ExternalDependencies']),
            'project_url': str(data['ProjectURL']),
            'maintainer': str(data['Maintainer']),
            'status': str(data['Status']),
            'license': str(data['License']),
            'environment_size': str(data['EnvironmentSize'])
        }

# parse_test_definition_settings
# Handles parsing the profile section of the test definition file
def parse_test_definition_settings(data):
    tOptions = []
    tMenuEntries = []
    for option in data['Option']:
        # Get the menu items
        tMenuEntries = []
        if option['Menu']['Entry']:
            # Loop through the option entries
            for entry in option['Menu']['Entry']:
                tMenuEntries.append(
                    {
                        'name': entry['Name'],
                        'value': entry['Value']
                    }
                )

        tOptions.append(
            {
                'display_name': option['DisplayName'],
                'identifier': option['Identifier'],
                'argument_prefix': option['ArgumentPrefix'],
                'menu': {
                    'entry': tMenuEntries
                }
            }
        )

    return {
        'args': str(data['Default']['Arguments']),
        'options': tOptions
    }

# parse_test_definition_file
# Handles parsing the test definition file
def parse_test_definition_file(benchmark_directory, benchmark, definition_file):
    # Hold the benchmark data for the passed item
    tDefs = {}
    try:
        # Set the full path to the benchmark
        tBenchmark = os.path.join(benchmark_directory, benchmark)

        # Set the full path to the benchmarks file
        tFilePath = os.path.join(tBenchmark, definition_file)

        if config.debug:
            click.echo('Opening file ' + tFilePath)

        # Open the JSON file that contains the download info
        with open(tFilePath) as data_file:
            # Load the JSON file
            tData = json.load(data_file)
            tDefs = {}
            jsonStart = 'BenchmarkSuite'

            tInfoName = 'TestInformation'
            tInfo = tData[jsonStart][tInfoName]

            tProfileName = 'TestProfile'
            tProfile = tData[jsonStart][tProfileName]

            tSettingsName = 'TestSettings'
            tSettings = tData[jsonStart][tSettingsName]

            # Parse the JSON file and put it in a Python var that's easier to work with.

            # Stuff the JSON content in a dictionary
            tDefs['info'] = parse_test_definition_info(tInfo)

            # Stuff the JSON content in a dictionary
            tDefs['profile'] = parse_test_definition_profile(tProfile)

            # Stuff the JSON content in a dictionary
            tDefs['settings'] = parse_test_definition_settings(tSettings)

        return tDefs

    except (KeyError, TypeError):
        click.echo('There was an issue finding benchmarks in this package.')
        return tDefs

# parse_downloads_file
# Parses the downloads.json (or whatever file set) and builds usable object
def parse_downloads_file(benchmark_directory, downloads_file, temporary_directory, item):
    # Hold the item data for the passed item
    tBenchmarks = {}
    try:
        # Set the full path to the benchmark
        tBenchmark = os.path.join(benchmark_directory, item)
        # Set the full path to the benchmarks file
        tFilePath = os.path.join(tBenchmark, downloads_file)

        # Open the JSON file that contains the download info
        with open(tFilePath) as data_file:
            # Load the JSON file
            tData = json.load(data_file)
            tBenchmarks[item] = []
            jsonStart = 'BenchmarkSuite'
            tPackage = tData[jsonStart]['Downloads']['Package']
            # Parse the JSON file and put it in a Python var that's easier to work with.
            for i in range(len(tPackage)):
                # Stuff the JSON content in a dictionary
                tBenchmarks[item].append({
                        'url': str(tPackage[i]['URL']),
                        'filesize': str(tPackage[i]['FileSize']),
                        'md5': str(tPackage[i]['MD5']),
                        'path': os.path.join(temporary_directory)
                    })
        return tBenchmarks[item]

    except (KeyError, TypeError):
        click.echo('There was an issue finding benchmarks in this package.')
        return tBenchmarks

# get_downloads
# Handles getting a single list of all benchmark file download urls
# config
# downloads\
def get_downloads(downloads):

    # Make a counter to track progress
    count = 0

    # Setup progress bar (w/Custom widget) for all files
    totalDownloads = int(len(downloads))
    cWidget = [ progressbar.Counter(), '/', str(totalDownloads), ' ', progressbar.Bar(), ' ', progressbar.Percentage() ]
    bar = progressbar.ProgressBar(maxval=totalDownloads, widgets=cWidget)

    # Start the bar
    bar.start()

    # Holds the download urls for all benchmark files
    file_urls = []

    # Traverse through the benchmarks
    for benchName in downloads:
        # Figure out path for the download to live at
        path = os.path.join(config.benchmark_directory, benchName)

        # Update the counter
        count = count + 1

        # Update the progress bar
        bar.update(count)

        # Traverse through the downloads for benchmarks
        for i in range(len(downloads[benchName])):
            if downloads[benchName][i]:
                # Run the download job to grab the file
                pre_download_job(path, downloads[benchName][i], config.max_buffer_size)
                # Figure out the total size of the file via the headers
                # file_size = int(downloads[benchName][i]['filesize'])
                # if config.debug:
                #     click.echo('Total file size: ' + str(file_size) )
                file_urls.append(downloads[benchName][i]['url'])

    # Finish the progress bar for this file
    bar.finish()
    return file_urls

# pre_download_job
# http://stackoverflow.com/questions/17285464/whats-the-best-way-to-download-file-using-urllib3
def pre_download_job(path, download, max_buffer_size):
    # Grab the file name
    fn = download['url'].split('/')[-1]

    # If the file already exists remove it
    file_helpers.remove_file(path, fn)

# setup_environment_variables
# Handles setting environment variables that are used by the benchmark install scripts.
def setup_environment_variables(config):
    # Set environment variables required for the benchmark scripts
    os.environ['TMP_DIR'] = config.temporary_directory

    # encode-flac
    os.environ['HOME'] = config.temporary_directory
    os.environ['NUM_CPU_JOBS'] = str(config.cpu_count)

    # himeno
    os.environ['OS_TYPE'] = config.sysname

    # For compiling tasks, try to use the most aggressive instructions possible
    os.environ['CFLAGS'] = '-march=native -O3'
    os.environ['CXXFLAGS'] = '-march=native -O3'

    # iozone
    # See http://stackoverflow.com/questions/2208828/detect-64bit-os-windows-in-python
    # if it becomes an issue figuring out 64 bit or not.
    """
    def is_os_64bit():
        return platform.machine().endswith('64')

    def Is64Windows():
        return 'PROGRAMFILES(X86)' in os.environ

    def GetProgramFiles32():
        if Is64Windows():
            return os.environ['PROGRAMFILES(X86)']
        else:
            return os.environ['PROGRAMFILES']

    def GetProgramFiles64():
        if Is64Windows():
            return os.environ['PROGRAMW6432']
        else:
            return None
    """
    os.environ['OS_ARCH'] = platform.architecture()[0]
    os.environ['LOG_FILE'] = os.path.abspath(os.path.join(config.log_directory, config.log_file))

# parse_package_file
# Handles pulling the contents of a benchmark package based on the package name passed.
def parse_package_file(package_directory, package_name):
    package = {}

    # Get the benchmark package path based on the name
    bpPath = os.path.join(package_directory, package_name)
    with open(bpPath) as p:
        bpData = json.load(p)
        jsonPackageParentName = 'BenchmarkPackage'
        # Parse the JSON file and put it in a Python var that's easier to work with.
        package = {
                'title': str(bpData[jsonPackageParentName]['Title']),
                'version': str(bpData[jsonPackageParentName]['Version']),
                'description': str(bpData[jsonPackageParentName]['Description']),
                'benchmarks': bpData[jsonPackageParentName]['Benchmarks']
            }
    return package

# install_benchmarks_in_package
# Handles running the install file in each of the benchmarks in a package.
def install_benchmarks_in_package(package, benchmark_directory, install_file):
    if package:
        return_codes = []
        for benchmark in package["benchmarks"]:
            # Run the install script
            install_file_full_path = get_full_path(
                    benchmark_directory,
                    install_file,
                    benchmark
                )
            if os.path.exists(install_file_full_path):
                return_code = call([install_file_full_path])
                return_codes.append({
                    benchmark : return_code
                })
            else:
                click.echo('Unable to run the install file. Check to ensure the file exists at ' + install_file)

        return return_codes
    else:
        click.echo('You need to supply a package variable.')
        return False


# get_full_path
# Handles returning a full path to the file passed
def get_full_path(directory, the_file, item=False):
    if item:
        return os.path.join(directory, item, the_file)
    else:
        return os.path.join(directory, the_file)

"""

END HELPER FUNCTIONS

"""

"""

CLICK COMMANDS

"""

# setup
# Main initialization point
@click.group()
@pass_config
@click.option('-d', '--debug', is_flag=True, help='Enables debug mode.')
@click.option('-p', '--package', default='default.json', help='Sets the default benchmark package to use.')
@click.option('--package-directory', default='packages', help='Sets the benchmark package directory.')
def setup(config, debug, package, package_directory):
    """Little Benchmark setup services."""
    if package_directory:
        config.package_directory = package_directory
    if package:
        config.default_package_file = package


# install
# Handles installing a single benchmark
@setup.command()
@pass_config
@click.option('-p', '--package', is_flag=True, help='Enables package install mode.')
@click.option('-b', '--benchmark', is_flag=True, help='Enables benchmark install mode.')
@click.argument('item', nargs=1, required=True)
@click.pass_context
def install(ctx, config, package, benchmark, item):
    """Helps install benchmark or package."""

    if benchmark:
        click.echo('Installing benchmark...')
        ctx.invoke(install_benchmark, benchmark=item)

    if package:
        click.echo('Installing package...')
        ctx.invoke(install_package, package=item)


# install_benchmark
# Handles installing a single benchmark
@setup.command()
@pass_config
@click.argument('benchmark', nargs=1, required=True)
def install_benchmark(config, benchmark):
    """Helps install a single benchmark."""

    # Generate the full path to the benchmark's installation file.
    install_file_full_path = get_full_path(
            config.benchmark_directory,
            config.install_file,
            benchmark
        )
    if os.path.exists(install_file_full_path):
        # Execute the file
        call([install_file_full_path])
    else:
        click.echo('Uh oh. That benchmark does not seem to exist. (-. -,)')

    # Clear the set environment variables
    # See https://docs.python.org/2/library/os.html
    os.environ.clear()

# install_package
# Handles installing a benchmark package
@setup.command()
@pass_config
@click.argument('package', nargs=1, required=True)
def install_package(config, package):
    """Helps install a benchmark package."""

    default_extension = '.json'

    # Add JSON extension
    filename, file_extension = os.path.splitext(package)
    if file_extension is '':
        package = package + default_extension

    # Generate the full path to the package file.
    package_file_full_path = get_full_path(
            config.package_directory,
            package
        )

    # Check to see if the package exists
    if os.path.exists(package_file_full_path) is False:

        click.echo('Uh oh. That package does not seem to exist. (-. -,)')

    else:

        # Remove the previous installation folder.
        file_helpers.remove_directory(config.install_path)

        # Rebuild the required folders
        make_required_folders(
                config.install_path,
                config.temporary_directory
            )

        # Parse the package file and grab benchmarks that need to be processed.
        parsed_package = parse_package_file(config.package_directory, package)

        # Download required files
        download_benchmarks(
                parsed_package['benchmarks'],
                config.benchmark_directory,
                config.downloads_file,
                config.temporary_directory,
                config.log_directory
            )


        # These environment variables are used by the benchmark install scripts
        setup_environment_variables(config)

        # pauseTime = 2
        # click.echo("Pausing for " + str(pauseTime) + " seconds.\n")
        # time.sleep(pauseTime)

        # Handles installing all of the benchmarks in a particular package.
        return_codes = install_benchmarks_in_package(
                parsed_package,
                config.benchmark_directory,
                config.install_file
            )

        click.echo(return_codes)

        # Clear the set environment variables
        # See https://docs.python.org/2/library/os.html
        os.environ.clear()

"""

END CLICK COMMANDS

"""
