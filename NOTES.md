# General Overview
- A test profile is a single test that can be executed by the Phoronix Test Suite -- with a series of options possible within every test
- A test suite is a seamless collection of test profiles and/or additional test suites.
- A test profile consists of a set of Bash/shell scripts and XML files while a test suite is a single XML file.

- Available through OpenBenchmarking.org, a collaborative storage platform developed in conjunction with the Phoronix Test Suite, are more than 200 individual test profiles and more than 60 test suites available by default from the Phoronix Test Suite.
- Independent users are also able to upload their test results, profiles, and suites to OpenBenchmarking.org.

- Phoronix Test Suite for interfacing with Phoronix Test Suite client(s) to automatically execute test runs on a timed, per-commit, or other trigger-driven basis.
- Phoromatic is designed for enterprise and allows for the easy management of multiple networked systems running Phoronix Test Suite clients via a single web-based interface.

- The process to download, install/setup, execute, and report the results of a benchmark can be as simple as a command such as phoronix-test-suite benchmark smallpt to run a simple CPU test profile.

- If wishing to simply install a test, it's a matter of running phoronix-test-suite install <test or suite name> and to run it's phoronix-test-suite run <test or suite name>.

# PHP Tracing and System Function Analysis

`$ phoronix-test-suite benchmark` `phoronix-test-suite/pts-core/commands/benchmark.php`
Runs the following command:
```
...
pts_test_installer::standard_install($r);
$run_manager = new pts_test_run_manager();
$run_manager->standard_run($r);
```

`pts_test_installer` lives inside of `phoronix-test-suite/pts-core/objects/client/pts_test_installer.php`

Inside of `pts_types::identifiers_to_test_profile_objects($items_to_install, true, true, $unknown_tests);` is where it links `$r` the benchmark type to a test profile. `pts_types.php` lives inside of `phoronix-test-suite/pts-core/objects`. This handles checking to see if the passed argument is either `pts_test_profile`, `pts_test_suite`, `pts_virtual_test_suite`, `pts_result_file`, or `pts_virtual_test_queue` and handles accordingly.

And then eventually finds its way to pulling the file `phoronix-test-suite/pts-core/openbenchmarking.org/schemas/types.xsd`

If it's a `pts_test_profile`, the methods inside of `pts_test_profile.php` take effect.

Besides all of the this, which basically appears to be gathering more details about the argument, the following line is run (after returning with details).

```
pts_external_dependencies::install_dependencies($test_profiles, $no_prompts, $skip_tests_with_missing_dependencies);
```

`pts_external_dependencies` lives in `phoronix-test-suite/pts-core/objects/client/pts_external_dependencies.php`.
This file checks for any system or other dependencies related to the passed module need to be installed. After all is said and done it finally runs one of the following commands in a switch statement:

```
case 'SKIP_TESTS_WITH_MISSING_DEPS':
	// Unset the tests that have dependencies still missing
	self::remove_tests_with_missing_dependencies($test_profiles, $generic_packages_needed, $required_external_dependencies);
	break;

case 'REATTEMPT_DEP_INSTALL':
	self::install_packages_on_system($dependencies_to_install);
	break;

```

```
private static function install_packages_on_system($os_packages_to_install)
{
	// Do the actual installing process of packages using the distribution's package management system
	$vendor_install_file = PTS_EXDEP_PATH . 'scripts/install-' . self::vendor_identifier('installer') . '-packages.sh';

	// Rebuild the array index since some OS package XML tags provide multiple package names in a single string
	$os_packages_to_install = explode(' ', implode(' ', $os_packages_to_install));

	if(is_file($vendor_install_file))
	{
		// hook into pts_client::$display here if it's desired
		echo PHP_EOL . 'The following dependencies are needed and will be installed: ' . PHP_EOL . PHP_EOL;
		echo pts_user_io::display_text_list($os_packages_to_install);
		echo PHP_EOL . 'This process may take several minutes.' . PHP_EOL;

		echo shell_exec('sh ' . $vendor_install_file . ' ' . implode(' ', $os_packages_to_install));
	}
	else
	{
		if(phodevi::is_macosx() == false)
		{
			echo 'Distribution install script not found!';
		}
	}
}

private static function vendor_identifier($type)
{
	$os_vendor = phodevi::read_property('system', 'vendor-identifier');

	switch($type)
	{
		case 'package-list':
			$file_check_success = is_file(PTS_EXDEP_PATH . 'xml/' . $os_vendor . '-packages.xml');
			break;
		case 'installer':
			$file_check_success = is_file(PTS_EXDEP_PATH . 'scripts/install-' . $os_vendor . '-packages.sh');
			break;
	}

	if($file_check_success == false)
	{
		// Check the aliases to figure out the upstream distribution
		$os_vendor = false;
		$exdep_generic_parser = new pts_exdep_generic_parser();
		foreach($exdep_generic_parser->get_vendors_list() as $this_vendor)
		{
			$exdep_platform_parser = new pts_exdep_platform_parser($this_vendor);
			$aliases = $exdep_platform_parser->get_aliases();

			if(in_array($os_vendor, $aliases))
			{
				$os_vendor = $this_vendor;
				break;
			}
		}

		if($os_vendor == false)
		{
			// Attempt to match the current operating system by seeing what package manager matches
			foreach($exdep_generic_parser->get_vendors_list() as $this_vendor)
			{
				$exdep_platform_parser = new pts_exdep_platform_parser($this_vendor);
				$package_manager = $exdep_platform_parser->get_package_manager();

				if($package_manager != null && pts_client::executable_in_path($package_manager))
				{
					$os_vendor = $this_vendor;
					break;
				}
			}
		}
	}

	return $os_vendor;
}
```

# Available Tests
You can find a list of tests and more details at http://openbenchmarking.org/tests/pts.

| Path | Name | Type |
| ---- | ---- | ---- |
| pts/apitest | APITest| Graphics |
| pts/arrayfire | ArrayFire | Processor |
| pts/blake2 | BLAKE2 | Processor|
| pts/blogbench | BlogBench | Disk |
| pts/bork | Bork File Encrypter | Processor |
| pts/botan | Botan | Processor |
| pts/build-apache | Timed Apache Compilation | Processor |
| pts/build-firefox | Timed Firefox Compilation | Processor |
| pts/build-imagemagick | Timed ImageMagick Compilation | Processor |
| pts/build-php | Timed PHP Compilation | Processor |
| pts/bullet | Bullet Physics Engine | Processor |
| pts/byte | BYTE Unix Benchmark | Processor |
| pts/c-ray | C-Ray | Processor |
| pts/clomp | CLOMP | Processor |
| pts/compilebench | Compile Bench | Disk |
| pts/compress-7zip | 7-Zip Compression | Processor |
| pts/compress-gzip | Gzip Compression |  Processor |
| pts/corebreach | CoreBreach | Graphics |
| pts/dcraw | dcraw | Processor |
| pts/encode-ape | Monkey | Audio Encoding |
| pts/encode-flac | FLAC | Audio Encoding |
| pts/encode-mp3 | LAME | MP3 Encoding |
| pts/encode-opus | Opus | Codec Encoding |
| pts/encode-wavpack | WavPack | Audio Encoding |
| pts/ffmpeg | FFmpeg | Processor |
| pts/fhourstones | Fhourstones | Processor |
| pts/graphics-magick | GraphicsMagick | Processor |
| pts/himeno | Himeno Benchmark | Processor |
| pts/hint | Hierarchical INTegration | System |
| pts/idle | Timed Idle | System |
| pts/iperf | iPerf | Network |
| pts/j2dbench | Java 2D Microbenchmark | Graphics |
| pts/java-scimark2 | Java SciMark | Processor |
| pts/jgfxbat | Java Graphics Basic Acceptance Test | Processor |
| pts/john-the-ripper | John The Ripper | Processor |
| pts/juliagpu | JuliaGPU | System |
| pts/mafft | Timed MAFFT Alignment | Processor |
| pts/mandelbulbgpu | MandelbulbGPU | System |
| pts/mandelgpu | MandelGPU | System |
| pts/mencoder | Mencoder | Processor |
| pts/minion| Minion | Processor |
| pts/mrbayes | Timed MrBayes Analysis | Processor |
| pts/multichase| Multichase Pointer Chaser | Processor |
| pts/netperf | Netperf | Network |
| pts/nexuiz| Nexuiz | Graphics |
| pts/nexuiz-iqc| Nexuiz Image Quality | System |
| pts/openarena | OpenArena | Graphics |
| pts/openssl | OpenSSL | Processor |
| pts/pgbench | PostgreSQL pgbench | System |
| pts/polybench-c | PolyBench-C | Processor |
| pts/postmark  | PostMark | Disk |
| pts/primesieve| Primesieve | Processor |
| pts/pts-self-test | Phoronix Test Suite Self Test | System |
| pts/pybench | PyBench | System |
| pts/qvdpautest | qVDPAUtestGraphics | |
| pts/sample-program| Sample Pi Program | Processor |
| pts/scimark2 | SciMark | Processor |
| pts/smallpt-gpu | SmallPT GPU | System |
| pts/sqlite| SQLite | Disk |
| pts/stockfish | Stockfish | Processor |
| pts/stream| Stream | Memory |
| pts/sudokut | Sudokut | Processor |
| pts/sunflow | Sunflow Rendering System | System |
| pts/t-test1 | t-test1 | Memory |
| pts/tachyon | Tachyon  | Processor |
| pts/tiobench | Threaded I/O Tester | Disk |
| pts/tjbench | libjpeg-turbo tjbench | System |
| pts/tscp  | TSCP | Processor |
| pts/unpack-linux | Unpacking The Linux Kernel | Disk |
| pts/unvanquished | Unvanquished | Graphics |
| pts/urbanterror | Urban Terror | Graphics |
| pts/xonotic | Xonotic | Graphics |
| pts/xplane9 | X-Plane | Graphics |
| pts/xplane9-iqc | X-Plane Image Quality | System |
| system/apache | Apache Benchmark |  |
| system/caffe | Caffe | |
| system/compress-lzma | LZMA Compression | |
| system/compress-pbzip2 | PBZIP2 Compression | |
| system/openssl | OpenSSL | |
| system/redis | Redis | |
| system/sqlite | SQLite | |


# Command Line Options

```
The *Phoronix Test Suite* is the most comprehensive testing and benchmarking platform available for Linux, Solaris, OS X, and BSD operating systems. The Phoronix Test Suite allows for carrying out tests in a fully automated manner from test installation to execution and reporting. All tests are meant to be easily reproducible, easy-to-use, and support fully automated execution. The Phoronix Test Suite is open-source under the GNU GPLv3 license and is developed by Phoronix Media in cooperation with partners.

View the included PDF / HTML documentation or visit http://www.phoronix-test-suite.com/ for full details.

TEST INSTALLATION

    install				        [Test | Suite | OpenBenchmarking ID | Test Result]  ...
    install-dependencies  [Test | Suite | OpenBenchmarking ID | Test Result]  ...
    make-download-cache
    remove-installed-test [Test]

TESTING

    auto-compare
    benchmark          [Test | Suite | OpenBenchmarking ID | Test Result]  ...
    finish-run         [Test Result]
    run                [Test | Suite | OpenBenchmarking ID | Test Result]  ...
    run-random-tests
    run-tests-in-suite
    stress-run         [Test | Suite | OpenBenchmarking ID | Test Result]  ...

BATCH TESTING

    batch-benchmark   [Test | Suite | OpenBenchmarking ID | Test Result]  ...
    batch-install     [Test | Suite | OpenBenchmarking ID | Test Result]  ...
    batch-run         [Test | Suite | OpenBenchmarking ID | Test Result]  ...
    batch-setup
    default-benchmark [Test | Suite | OpenBenchmarking ID | Test Result]  ...
    default-run       [Test | Suite | OpenBenchmarking ID | Test Result]  ...
    internal-run      [Test | Suite | OpenBenchmarking ID | Test Result]  ...

OPENBENCHMARKING.ORG

    clone-result                  [OpenBenchmarking ID]  ...
    list-recommended-tests
    make-openbenchmarking-cache
    openbenchmarking-changes
    openbenchmarking-launcher
    openbenchmarking-login
    openbenchmarking-refresh
    openbenchmarking-repositories
    upload-result                 [Test Result]
    upload-test-profile
    upload-test-suite

SYSTEM

    diagnostics
    interactive
    php-conf
    system-info
    system-sensors

INFORMATION

    estimate-run-time             [Test | Suite | OpenBenchmarking ID | Test Result]
    info                          [Test | Suite | OpenBenchmarking ID | Test Result]
    list-available-suites
    list-available-tests
    list-available-virtual-suites
    list-installed-dependencies
    list-installed-suites
    list-installed-tests
    list-missing-dependencies
    list-not-installed-tests
    list-possible-dependencies
    list-saved-results
    list-test-usage
    list-unsupported-tests

ASSET CREATION

    debug-benchmark           [Test | Suite | OpenBenchmarking ID | Test Result]  ...
    debug-install             [Test | Suite | OpenBenchmarking ID | Test Result]  ...
    debug-result-parser       [Test | Suite | OpenBenchmarking ID | Test Result]  ...
    debug-test-download-links [Test | Suite | OpenBenchmarking ID | Test Result]
    download-test-files       [Test | Suite | OpenBenchmarking ID | Test Result]  ...
    force-install             [Test | Suite | OpenBenchmarking ID | Test Result]  ...
    result-file-to-suite      [Test Result]
    validate-result-file
    validate-test-profile
    validate-test-suite

RESULT MANAGEMENT

    auto-sort-result-file            [Test Result]
    edit-result-file                 [Test Result]
    extract-from-result-file         [Test Result]
    merge-results                    [Test Result]  ...
    refresh-graphs                   [Test Result]
    remove-from-result-file          [Test Result]
    remove-result                    [Test Result]
    rename-identifier-in-result-file [Test Result]
    rename-result-file               [Test Result]
    reorder-result-file              [Test Result]
    result-file-to-csv               [Test Result]
    result-file-to-json              [Test Result]
    result-file-to-pdf               [Test Result]
    result-file-to-text              [Test Result]
    show-result                      [Test Result]
    winners-and-losers               [Test Result]

RESULT ANALYTICS

    analyze-all-runs [Test Result]

OTHER

    build-suite
    debug-dependency-handler
    debug-render-test
    debug-self-test
    enterprise-setup
    help
    network-setup
    user-config-reset
    user-config-set
    version

WEB / GUI SUPPORT

    gui
    start-remote-gui-server
    start-ws-server

MODULES

    list-modules
    module-info  [Phoronix Test Suite Module]
    module-setup [Phoronix Test Suite Module]
    test-module  [Phoronix Test Suite Module]

PHOROMATIC

    start-phoromatic-server
```

# Test Install Results

`$ phoronix-test-suite install apitest`
```
## Phoronix Test Suite v7.0.0

    To Install: pts/apitest-1.1.0

    Determining File Requirements ..........................................................................................................................................
    Searching Download Caches ..............................................................................................................................................

    1 Test To Install
        1 File To Download [22.75MB]
        225MB Of Disk Space Is Needed

    pts/apitest-1.1.0:
        Test Installation 1 of 1
        1 File Needed [22.75 MB]
        Downloading: apitest-20140726.tar.bz2                                                                                                                      [22.75MB]
        Downloading ........................................................................................................................................................
        Installation Size: 225 MB
        Installing Test @ 18:57:32
```

## File installed into:
```
~/.phoronix-test-suite/openbenchmarking.org/pts/apitest-1.1.0.zip
~/.phoronix-test-suite/test-profiles/pts/apitest-1.1.0
~/.phoronix-test-suite/test-profiles/pts/apitest-1.1.0/downloads.xml
~/.phoronix-test-suite/test-profiles/pts/apitest-1.1.0/install.sh
~/.phoronix-test-suite/test-profiles/pts/apitest-1.1.0/results-definition.xml
~/.phoronix-test-suite/test-profiles/pts/apitest-1.1.0/test-definition.xml
```
![](https://s12.postimg.org/anr8yy4c9/Screen_Shot_2017-03-28_at_3.01.22_PM.png|thumbnail)
![](https://s12.postimg.org/ovgxnlh15/Screen_Shot_2017-03-28_at_3.01.32_PM.png|thumbnail)

Inside of the hidden folders are folders that contain the following set of files:
- downloads.xml
	- Contains links to tar packages that contain the actual test code.
- install.sh
	- Shell script that handles installing the test
- post.sh
	- Assuming this runs after the install
- pre.sh
	- Assuming this runs right before the install begins
- results-definition.xml
	- Contains file and download stats related to the test code
- test-definition.xml
	- Contains test information, test profile, and test settings
