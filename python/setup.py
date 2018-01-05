"""
Little Benchmark is a python CLI (Command Line Interface) tool for benchmarking microchips.
"""
from setuptools import find_packages, setup

dependencies = [
	'click','multiprocessing','progressbar','urllib3','pycurl'
]

setup(
	name='lb',
	version='1.0.1',
	url='https://github.com/robksawyer/lb',
	license='Commercial',
	author='Rob Sawyer',
	author_email='rob@siliconunited.com',
	description='Little Benchmark is a Python CLI (Command Line Interface) tool for benchmarking microchips.',
	long_description=__doc__,
	packages=find_packages(exclude=['tests']),
	include_package_data=True,
	zip_safe=False,
	platforms='any',
	install_requires=dependencies,
	entry_points='''
		[console_scripts]
		lb = lb.cli:main
	''',
	classifiers=[
		# As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
		# 'Development Status :: 1 - Planning',
		# 'Development Status :: 2 - Pre-Alpha',
		# 'Development Status :: 3 - Alpha',
		'Development Status :: 4 - Beta',
		# 'Development Status :: 5 - Production/Stable',
		# 'Development Status :: 6 - Mature',
		# 'Development Status :: 7 - Inactive',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: Commercial License',
		'Operating System :: POSIX',
		'Operating System :: MacOS',
		'Operating System :: Unix',
		'Operating System :: Microsoft :: Windows',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		# 'Programming Language :: Python :: 3',
		'Topic :: Software Development :: Libraries :: Python Modules'
	]
)
