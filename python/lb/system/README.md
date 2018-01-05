# System Commands
> This set of commands deals with setting configuration details that are used in other portions of the CLI.

# Getting started

To see an example of some system details, run the command: `lb system config`.

```
Usage: lb system [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --verbose                   Enables verbose mode.
  -d, --debug                     Enables debug mode.
  --benchmark-directory PATH      Sets the path to the benchmark directory.
  --install-file TEXT             Sets the benchmark install shell command to
                                  run.
  --downloads-file TEXT           Sets the file containing benchmark download
                                  information.
  --install-path TEXT             Sets the install path for the benchmark
                                  dependencies.
  --temporary-directory-root PATH
                                  Sets the root path to the temporary
                                  directory.
  --temporary-directory PATH      Sets the path to the temporary directory.
  --setup-file PATH               Points to the benchmark setup file.
  --version                       Show the version and exit.
  --help                          Show this message and exit.

Commands:
  config  Shows the current config settings
  info    More info about the CLI.

```
