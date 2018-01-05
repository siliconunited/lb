# config.py
# Handles setting up configuration variables that are used in other commands across the CLI.
import click
import platform
import sys
import os
import pkg_resources
import ssl
import multiprocessing

from lb.helpers import system

class Config(object):
    def __init__(self):
        self.debug = False
        self.verbose = False
        self.max_buffer_size = 32 # 32 KB
        self.version = pkg_resources.require('lb')[0].version
        self.codename = 'Monkey'
        self.url1 = 'http://www.littlebenchmark.com/'
        self.url2 = 'http://www.siliconunited.com/'
        self.sys = sys.platform
        self.sysname = system.get_sys_name(sys.platform)
        self.osname = os.name
        self.uname = os.uname()
        self.ssl_version = ssl.OPENSSL_VERSION
        self.cpu_count = multiprocessing.cpu_count()
        self.install_path = os.path.abspath('.littlebenchmark')
        self.install_file = 'install.sh'
        self.downloads_file = 'downloads.json'
        self.definition_file = 'test-definition.json'
        self.result_definition_file = 'results-definition.json'
        self.default_package_file = 'default.json'
        self.package_directory = 'packages'
        self.benchmark_directory = 'benchmarks'
        self.log_directory = 'logs'
        self.log_file = 'debug.log'
        self.temporary_directory = os.path.abspath('.littlebenchmark')



# ensure=True - ensures the Config is created automatically if it doesn't exist
pass_config = click.make_pass_decorator(Config, ensure=True)
